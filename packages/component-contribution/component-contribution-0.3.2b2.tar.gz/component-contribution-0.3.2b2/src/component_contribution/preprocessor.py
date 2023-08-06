"""calculations needed for component-contribution predictions."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from typing import Dict, List, Tuple

import numpy as np
from equilibrator_cache import Compound, Reaction
from scipy.linalg import sqrtm

from . import CCModelParameters
from .linalg import LINALG


class Preprocessor(object):
    """A Component Contribution preprocessing class."""

    DEFAULT_MSE_INF = 1e10

    def __init__(
        self, parameters: CCModelParameters, mse_inf: float = DEFAULT_MSE_INF
    ) -> None:
        """Create a GibbsEnergyPredictor object.

        Parameters
        ----------
        parameters : CCModelParameters
            all the parameters needed for running Component Contribution
            predictions.
        mse_inf : float
            The MSE of the subspace that's not covered by Component Contribution
            which is set as an arbitrary high value. By default we set it to
            10^10 (kJ^2 / mol^2)

        """
        self._compound_ids = parameters.train_G.index.tolist()
        self.Nc = parameters.dimensions.at["Nc", "number"]

        # store the number of "real" groups, i.e. not including the "fake"
        # ones that are placeholders for non-decomposable compounds
        self.Ng = parameters.dimensions.at["Ng", "number"]

        # the total number of groups ("real" and "fake")
        self.Ng_full = parameters.dimensions.at["Ng_full", "number"]

        W = np.diag(parameters.train_w.ravel())

        self.S = parameters.train_S.values
        self.G = parameters.train_G.values

        _, P_col = LINALG.col_uniq(self.S)
        self.S_counter = np.sum(P_col, 0)

        self.MSE_rc = parameters.MSE.at["rc", "MSE"]
        self.MSE_gc = parameters.MSE.at["gc", "MSE"]
        self.MSE_inf = mse_inf

        self.v_rc = parameters.dG0_cc
        self.v_gc = parameters.dG0_gc[: self.Ng]

        # pre-processing matrices
        self.G1 = parameters.P_R_rc @ parameters.inv_S.T @ W @ P_col
        self.G2 = parameters.P_N_rc @ self.G @ parameters.inv_GS.T @ W @ P_col
        self.G3 = parameters.inv_GS.T @ W @ P_col

        C1 = (
            self.MSE_rc * parameters.V_rc
            + self.MSE_gc * parameters.V_gc
            + self.MSE_inf * parameters.V_inf
        )
        C2 = (
            self.MSE_gc * parameters.P_N_rc @ self.G @ parameters.inv_GSWGS
            + self.MSE_inf * self.G @ parameters.P_N_gc
        )
        C3 = (
            self.MSE_gc * parameters.inv_GSWGS
            + self.MSE_inf * parameters.P_N_gc
        )
        C = np.block([[C1, C2], [C2.T, C3]])
        C = C[: (self.Nc + self.Ng), : (self.Nc + self.Ng)]
        M = sqrtm(C).real

        self.M_rc = M[: self.Nc, :]
        self.M_gc = M[self.Nc :, :]

    def get_compound_index(self, compound: Compound) -> int:
        """Get the index of a compound in the original training data.

        Parameters
        ----------
        compound : Compound
            a Compound object


        Returns
        -------
        int
            the index of that compound, or -1 if it was not in the
            training list

        """
        if compound.id in self._compound_ids:
            return self._compound_ids.index(compound.id)
        else:
            return -1

    def decompose_reaction(
        self, reaction: Reaction
    ) -> Tuple[np.ndarray, np.ndarray, Dict[Compound, float]]:
        """Decompose a reaction.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        tuple
            a tuple (x, g, residual) of the stoichiometric vector and
            group incidence vector, and the residual reaction
            in sparse notation

        """
        x = np.zeros(self.Nc)  # stoichiomtric vector for the RC part
        g = np.zeros(self.Ng)  # group vector for the GC part
        residual = dict()

        for compound, coefficient in reaction.items(protons=False):
            i = self.get_compound_index(compound)
            if i >= 0:
                # This compound is in the training set so we can use reactant
                # contributions for it
                x[i] = coefficient
            elif not compound.group_vector:
                residual[compound] = coefficient
            else:
                g += coefficient * np.array(
                    compound.group_vector, ndmin=1, dtype=float
                )
        return x, g, residual

    def get_compound_prediction(
        self, compound: Compound
    ) -> Tuple[float, np.ndarray]:
        """Get the (mu, sigma) predictions of a compound's formation energy."""
        i = self.get_compound_index(compound)
        if i >= 0:
            # This compound is in the training set so we can use reactant
            # contributions for it
            return self.v_rc[i], self.M_rc[i, :]
        elif compound.group_vector:
            g = np.array(compound.group_vector, dtype=float)
            return g @ self.v_gc, g @ self.M_gc
        else:
            return None, None

    def get_reaction_prediction(
        self, reaction: Reaction
    ) -> Tuple[float, np.ndarray, Dict[Compound, float]]:
        """Get the (mu, sigma) predictions of a reaction's energy.

        Parameters
        ----------
        reaction : Reaction
            the input Reaction object


        Returns
        -------
        mu : float
            the mean of the standard Gibbs energy estimate
        sigma : array
            a vector representing the square root of the covariance matrix
            (uncertainty)
        residual : dict
            the residual reaction in sparse notation (unknown and
            undecomposable reactants)

        """
        tot_mu = 0.0  # mean of the delta G estimate
        tot_sigma = np.zeros(self.Nc + self.Ng)  # sqrt uncertainty vector
        residual = dict()

        for compound, coefficient in reaction.items(protons=False):
            mu, sigma = self.get_compound_prediction(compound)
            if mu is not None:
                tot_mu += coefficient * mu
                tot_sigma += coefficient * sigma
            else:
                residual[compound] = coefficient

        return tot_mu, tot_sigma, residual

    def get_reaction_prediction_multi(
        self, reactions: List[Reaction]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Get the (mu, sigma) predictions of a reaction's energy.

        Parameters
        ----------
        reactions: List[Reaction] :
            a list of Reaction objects


        Returns
        -------
        mus : np.array
            the mean of the standard Gibbs energy estimates
        sigmas : np.array
            a matrix whose columns are the square root vectors (one for each
            reaction)
        residual : np.array
            another matrix with the square root of the covariance corresponding
            to the 'unknown' compounds (i.e. where the uncertainty is infinite)

        """
        Nr = len(reactions)
        mus = np.zeros(Nr)
        sigmas = np.zeros((Nr, self.Nc + self.Ng))

        residuals = []
        for i, reaction in enumerate(reactions):
            mu, sigma, residual = self.get_reaction_prediction(reaction)
            mus[i] = mu
            sigmas[i, :] = sigma
            residuals.append(residual)

        # make an ordered list of the unknown-undecomposable compounds
        residual_compounds = set()
        for sparse in residuals:
            residual_compounds.update(sparse.keys())
        residual_compounds = sorted(residual_compounds)

        # construct the residual stoichiometric matrix U
        U = np.zeros((len(residual_compounds), Nr))
        for i, sparse in enumerate(residuals):
            for cpd, coeff in sparse.items():
                j = residual_compounds.index(cpd)
                U[j, i] = coeff

        return mus, sigmas, np.sqrt(self.MSE_inf) * U
