# The MIT License (MIT)
#
# Copyright (c) 2013 Weizmann Institute of Science
# Copyright (c) 2018-2020 Institute for Molecular Systems Biology,
# ETH Zurich
# Copyright (c) 2018-2020 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark
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

from typing import Callable, Optional, Tuple

import numpy as np
import pandas as pd
from equilibrator_api import Q_, R, default_T
from scipy.optimize import Bounds, minimize

from .util import ECF_DEFAULTS


class EnzymeCostFunction(object):

    ECF_LEVEL_NAMES = [
        "capacity [M]",
        "thermodynamic",
        "saturation",
        "allosteric",
    ]
    CONFIDENCE_INTERVAL = 1.96  # TODO: move to params dict
    MINIMAL_STDEV = 1e-3  # TODO: move to params dict
    QUAD_REGULARIZATION_COEFF = 0.2
    EPSILON = 1e-9

    def __init__(
        self,
        S: np.ndarray,
        fluxes: Q_,
        kcat: Q_,
        standard_dg: Q_,
        KMM: Q_,
        ln_conc_lb: np.ndarray,
        ln_conc_ub: np.ndarray,
        mw_enz: Optional[Q_] = None,
        mw_met: Optional[Q_] = None,
        A_act: Optional[np.ndarray] = None,
        A_inh: Optional[np.ndarray] = None,
        K_act: Optional[Q_] = None,
        K_inh: Optional[Q_] = None,
        idx_water: int = -1,
        params: Optional[dict] = None,
    ):
        """Create a Cost Function object.

        Parameters
        ----------
        S: ndarray
            stoichiometric matrix [unitless]
        fluxes: Quantity [concentration]/[time]
            steady-state fluxes [flux units]
        kcat: Quantity [1/time]
            turnover numbers
        standard_dg: Quantity [energy]/[substance]
            standard Gibbs free energies of reaction
        KMM: Quantity [concentration]
            Michaelis-Menten coefficients
        ln_conc_lb: ndarray
            lower bounds on metabolite concentrations [ln M]
        ln_conc_ub: ndarray
            upper bounds on metabolite concentrations [ln M]
        mw_enz: Quantity, optional [mass]
            enzyme molecular weights
        mw_met: Quantity, optional [mass]
            metabolite molecular weights
        A_act: ndarray, optional
            Hill coefficient matrix of allosteric activators
        A_inh: ndarray, optional
            Hill coefficient matrix of allosteric inhibitors
        K_act: Quantity, optional [concentration]
            affinity coefficient matrix of allosteric activators
        K_inh: Quantity, optional [concentration]
            affinity coefficient matrix of allosteric inhibitors
        idx_water: int
            the index of water in the stoichiometric matrix (or -1
            if water is not part of the model)
        params: dict, optional
            dictionary of extra parameters
        """
        self.params = dict(ECF_DEFAULTS)
        if params is not None:
            self.params.update(params)

        self.S = S
        self.idx_water = idx_water

        if fluxes.check("[concentration]/[time]"):
            self.fluxes = fluxes.m_as("M/s").flatten()
        elif fluxes.unitless:
            # relative fluxes are dimensionless
            self.fluxes = fluxes.m_as("").flatten()
        else:
            raise ValueError("Fluxes must be in units of M/s or dimensionless")

        assert kcat.check("1/[time]")
        self.kcat = kcat.m_as("1/s").flatten()

        assert standard_dg.check("[energy]/[substance]")
        self.standard_dg_over_rt = (
            (standard_dg / (R * default_T)).m_as("").flatten()
        )

        assert KMM.check("[concentration]")
        self.KMM = KMM.m_as("M")

        self.ln_conc_lb = ln_conc_lb.flatten()
        self.ln_conc_ub = ln_conc_ub.flatten()

        # In MDMC we use Z-score to describe distribution within the metabolite
        # so we need to convert the "hard" bounds into a Gaussian distribution
        # we assume that the given bounds represent the 95% confidence interval
        # a the Gaussian distribution (i.e. [mu - 1.96*sigma, mu + 1.96*sigma])
        # Therefore:
        #              mu = (ub + lb) / 2
        #           sigma = (ub - lb) / 3.92
        self.ln_conc_mu = (self.ln_conc_ub + self.ln_conc_lb) / 2.0
        self.ln_conc_sigma = (self.ln_conc_ub - self.ln_conc_lb) / (
            self.CONFIDENCE_INTERVAL * 2.0
        )

        self.Nc, self.Nr = S.shape
        assert self.fluxes.shape == (self.Nr,)
        assert self.kcat.shape == (self.Nr,)
        assert self.standard_dg_over_rt.shape == (self.Nr,)
        assert self.KMM.shape == (self.Nc, self.Nr)
        assert self.ln_conc_lb.shape == (self.Nc,)
        assert self.ln_conc_ub.shape == (self.Nc,)

        self.cids = ["C%04d" % i for i in range(self.Nc)]

        self.S_subs = abs(self.S)
        self.S_prod = abs(self.S)
        self.S_subs[self.S > 0] = 0
        self.S_prod[self.S < 0] = 0

        # if the kcat source is 'gmean' we need to recalculate the
        # kcat_fwd using the formula:
        # kcat_fwd = kcat_gmean * sqrt(kEQ * prod_S(KMM) / prod_P(KMM))

        if self.params["kcat_source"] == "gmean":
            ln_KMM_prod = np.array(np.diag(self.S.T @ np.log(self.KMM)))
            ln_ratio = -ln_KMM_prod - self.standard_dg_over_rt
            factor = np.sqrt(np.exp(ln_ratio))
            self.kcat *= factor

        # molecular weights of enzymes and metabolites
        if mw_enz is None:
            self.mw_enz = np.ones(self.Nr)
        else:
            assert mw_met.check("[mass]")
            self.mw_enz = mw_enz.m_as("Da").flatten()
            assert self.mw_enz.shape == (self.Nr,)

        if mw_met is None:
            self.mw_met = np.ones(self.Nc)
        else:
            assert mw_met.check("[mass]")
            self.mw_met = mw_met.m_as("Da").flatten()
            assert self.mw_met.shape == (self.Nc,)

        # allosteric regulation term

        if A_act is None or K_act is None:
            self.A_act = np.zeros(S.shape)
            self.K_act = np.ones(S.shape)
        else:
            assert S.shape == A_act.shape
            assert S.shape == K_act.shape
            assert K_act.check("[concentration]")
            self.A_act = A_act
            self.K_act = K_act.m_as("M")

        if A_inh is None or K_inh is None:
            self.A_inh = np.zeros(S.shape)
            self.K_inh = np.ones(S.shape)
        else:
            assert S.shape == A_inh.shape
            assert S.shape == K_inh.shape
            assert K_inh.check("[concentration]")
            self.A_inh = A_inh
            self.K_inh = K_inh.m_as("M")

        # if one of the compounds is water, we remove its effect on the
        # saturation, and the MW cost of metabolites
        if self.idx_water > -1:
            self.S_subs[self.idx_water, :] = 0
            self.S_prod[self.idx_water, :] = 0
            self.mw_met[self.idx_water] = 0

        # preprocessing: these auxiliary matrices help calculate the ECF3 and
        # ECF4 faster
        self.D_S_coeff = np.diag(self.S_subs.T @ np.log(self.KMM))
        self.D_P_coeff = np.diag(self.S_prod.T @ np.log(self.KMM))
        self.act_denom = np.diag(self.A_act.T @ np.log(self.K_act))
        self.inh_denom = np.diag(self.A_inh.T @ np.log(self.K_inh))

        try:
            self.ECF = eval("self._ECF%s" % self.params["version"])
        except AttributeError:
            raise ValueError(
                "The enzyme cost function %d is unknown"
                % self.params["version"]
            )

        try:
            self.D = eval("self._D_%s" % self.params["denominator"])
        except AttributeError:
            raise ValueError(
                "The denominator function %s is unknown"
                % self.params["denominator"]
            )

        self.regularization = self.params["regularization"]

    def _reshape_ln_conc(self, ln_conc) -> np.ndarray:
        """Adjust the dimentionality of the ln_conc array."""
        if isinstance(ln_conc, list):
            return np.array(ln_conc, dtype=float, ndmin=2).T
        if isinstance(ln_conc, np.ndarray):
            assert ln_conc.ndim <= 2
            if ln_conc.ndim == 2:
                assert ln_conc.shape[0] == self.Nc
                return ln_conc
            else:
                assert ln_conc.size == self.Nc
                return ln_conc.reshape(self.Nc, 1)
        else:
            raise TypeError(f"Unknown type for ln_conc: {type(ln_conc)}")

    def get_driving_forces(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            calculate the driving force for every reaction in every condition
        """
        if ln_conc.ndim == 2:
            n = ln_conc.shape[1]
            return (
                -np.tile(self.standard_dg_over_rt, (n, 1)).T
                - self.S.T @ ln_conc
            )
        else:
            return -self.standard_dg_over_rt - self.S.T @ ln_conc

    def _eta_thermodynamic(self, ln_conc: np.ndarray) -> np.ndarray:
        driving_force = self.get_driving_forces(ln_conc)

        # replace infeasbile reactions with a positive driving force to avoid
        # negative cost in ECF2
        eta_thermo = 1.0 - np.exp(-driving_force)

        # set the value of eta to a negative number when the reaction is
        # infeasible so it will be easy to find them, and also calculating
        # 1/x will not return an error
        eta_thermo[driving_force <= 0] = -1.0
        return eta_thermo

    def _D_S(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            return a matrix containing the values of D_S
            i.e. prod(s_i / K_i)^n_i

            each row corresponds to a reaction in the model
            each column corresponds to another set of concentrations (assuming
            ln_conc is a matrix)
        """
        if ln_conc.ndim == 2:
            n = ln_conc.shape[1]
            return np.exp(
                self.S_subs.T @ ln_conc - np.tile(self.D_S_coeff, (n, 1)).T
            )
        else:  # TODO: test this new code
            return np.exp(self.S_subs.T @ ln_conc - self.D_S_coeff)

    def _D_SP(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            return a matrix containing the values of D_SP
            i.e. prod(s_i / K_i)^n_i + prod(p_j / K_j)^n_j

            each row corresponds to a reaction in the model
            each column corresponds to another set of concentrations (assuming
            ln_conc is a matrix)
        """
        if ln_conc.ndim == 2:
            n = ln_conc.shape[1]
            return np.exp(
                self.S_subs.T @ ln_conc - np.tile(self.D_S_coeff, (n, 1)).T
            ) + np.exp(
                self.S_prod.T @ ln_conc - np.tile(self.D_P_coeff, (n, 1)).T
            )
        else:  # TODO: test this new code
            return np.exp(self.S_subs.T @ ln_conc - self.D_S_coeff) + np.exp(
                self.S_prod.T @ ln_conc - self.D_P_coeff
            )

    def _D_1S(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            return a matrix containing the values of D_1S
            i.e. 1 + prod(s_i / K_i)^n_i

            each row corresponds to a reaction in the model
            each column corresponds to another set of concentrations (assuming
            ln_conc is a matrix)
        """
        return 1.0 + self._D_S(ln_conc)

    def _D_1SP(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            return a matrix containing the values of D_1SP
            i.e. 1 + prod(s_i / K_i)^n_i + prod(p_j / K_j)^n_j

            each row corresponds to a reaction in the model
            each column corresponds to another set of concentrations (assuming
            ln_conc is a matrix)
        """
        return 1.0 + self._D_SP(ln_conc)

    def _D_CM(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            return a matrix containing the values of D_CM
            i.e. prod(1 + s_i / K_i)^n_i + prod(1 + p_j / K_j)^n_j - 1

            each row corresponds to a reaction in the model
            each column corresponds to another set of concentrations (assuming
            ln_conc is a matrix)
        """
        if ln_conc.ndim == 2:
            n = ln_conc.shape[1]
            D = np.zeros((self.Nr, n))
            for k in range(n):
                X_k = np.log(
                    np.exp(np.tile(ln_conc[:, k], (self.Nr, 1)).T) / self.KMM
                    + 1.0
                )
                ln_1_plus_S = np.diag(self.S_subs.T @ X_k)
                ln_1_plus_P = np.diag(self.S_prod.T @ X_k)
                D[:, k] = np.exp(ln_1_plus_S) + np.exp(ln_1_plus_P) - 1.0
            return D
        else:  # TODO: test this new code
            X = np.log(
                np.exp(np.tile(ln_conc, (self.Nr, 1)).T) / self.KMM + 1.0
            )
            ln_1_plus_S = np.diag(self.S_subs.T @ X)
            ln_1_plus_P = np.diag(self.S_prod.T @ X)
            D = np.exp(ln_1_plus_S) + np.exp(ln_1_plus_P) - 1.0
            return D

    def _eta_kinetic(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            the kinetic part of ECF3 and ECF4
        """
        return self._D_S(ln_conc) / self.D(ln_conc)

    def _eta_allosteric(self, ln_conc: np.ndarray) -> np.ndarray:
        if ln_conc.ndim == 2:
            n = ln_conc.shape[1]
            kin_act = np.exp(
                -self.A_act.T @ ln_conc + np.tile(self.act_denom, (n, 1)).T
            )
            kin_inh = np.exp(
                self.A_inh.T @ ln_conc - np.tile(self.inh_denom, (n, 1)).T
            )
        else:  # TODO: test this new code
            kin_act = np.exp(-self.A_act.T @ ln_conc + self.act_denom)
            kin_inh = np.exp(self.A_inh.T @ ln_conc - self.inh_denom)
        eta_kin = 1.0 / (1.0 + kin_act) / (1.0 + kin_inh)
        return eta_kin

    def is_feasible(self, ln_conc: np.ndarray) -> bool:
        df = self.get_driving_forces(ln_conc)
        return (df > 0).all()

    def get_v_max(self, E):
        """
            calculate the maximal rate of each reaction, kcat is in
            umol/min/mg and E is in gr, so we multiply by 1000

            Returns:
                Vmax  - in units of [umol/min]
        """
        assert E.shape == (self.Nr,)
        return self.kcat * E  # in M/s

    def _ECF1(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            Arguments:
                A single metabolite ln-concentration vector

            Returns:
                The most basic Enzyme Cost Function (only dependent on flux
                and kcat). Gives the predicted enzyme concentrations in [M]
        """
        # ln_conc is not used for ECF1, except to determine the size of the result
        # matrix.
        if ln_conc.ndim == 2:
            ecf1 = np.tile(self.fluxes / self.kcat, (ln_conc.shape[1], 1)).T
        else:
            ecf1 = self.fluxes / self.kcat
        return ecf1

    def _ECF2(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            Arguments:
                A single metabolite ln-concentration vector

            Returns:
                The thermodynamic-only Enzyme Cost Function.
                Gives the predicted enzyme concentrations in [M].
        """
        ecf2 = self._ECF1(ln_conc) / self._eta_thermodynamic(ln_conc)
        # fix the "fake" values that were given in ECF2 to infeasible reactions
        ecf2[ecf2 < 0] = np.nan
        return ecf2

    def _ECF3(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            Arguments:
                A single metabolite ln-concentration vector

            Returns:
                An Enzyme Cost Function that integrates kinetic and
                thermodynamic data, but no allosteric regulation.
                Gives the predicted enzyme concentrations in [M].
        """
        # calculate the product of all substrates and products for the kinetic
        # term
        ecf3 = self._ECF2(ln_conc) / self._eta_kinetic(ln_conc)
        return ecf3

    def _ECF4(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            Arguments:
                A single metabolite ln-concentration vector

            Returns:
                The full Enzyme Cost Function, i.e. with kinetic, thermodynamic
                and allosteric data.
                Gives the predicted enzyme concentrations in [M].
        """
        ecf4 = self._ECF3(ln_conc) / self._eta_allosteric(ln_conc)
        return ecf4

    def get_enzyme_cost_partitions(self, ln_conc: np.ndarray) -> np.ndarray:
        """
            Arguments:
                A single metabolite ln-concentration vector

            Returns:
                A matrix contining the enzyme costs separated to the 4 ECF
                factors (as columns).
                The first column is the ECF1 predicted concentrations in [M].
                The other columns are unitless (added cost, always > 1)
        """
        cap = self._ECF1(ln_conc)  # capacity
        trm = 1.0 / self._eta_thermodynamic(ln_conc)  # thermodynamics
        kin = 1.0 / self._eta_kinetic(ln_conc)  # kinetics
        alo = 1.0 / self._eta_allosteric(ln_conc)  # allostery
        return np.vstack([cap.flat, trm.flat, kin.flat, alo.flat]).T

    def get_volumes(self, ln_conc: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
            Arguments:
                A single metabolite ln-concentration vector

            Returns:
                Two arrays containing the enzyme volumes and
                metabolite volumes (at the provided point)
        """
        enz_conc = self.ECF(ln_conc)
        met_conc = np.exp(ln_conc)
        enz_vols = np.multiply(enz_conc.flat, self.mw_enz.flat)
        met_vols = np.multiply(met_conc.flat, self.mw_met.flat)
        return enz_vols, met_vols

    def get_fluxes(self, ln_conc: np.ndarray, E: np.ndarray) -> np.ndarray:
        assert E.shape == (self.Nr,)

        if ln_conc.ndim == 2:
            v = np.tile(self.get_v_max(E), (ln_conc.shape[1], 1)).T
        else:
            v = self.get_v_max(E)
        v *= self._eta_thermodynamic(ln_conc)
        v *= self._eta_kinetic(ln_conc)
        v *= self._eta_allosteric(ln_conc)
        return v

    def _enzyme_cost_objective(self, ln_conc: np.ndarray) -> float:
        """Calculate the enzyme cost for an input concentration profile."""
        ec = float(np.dot(self.ECF(ln_conc).flat, self.mw_enz.flat))
        if np.isnan(ec) or ec <= 0:
            raise Exception(
                "ECF returns NaN although all reactions are feasible"
            )
        return ec

    def _metabolite_cost_objective(self, ln_conc: np.ndarray) -> float:
        """Calculate the enzyme cost for an input concentration profile."""
        return float(np.dot(np.exp(ln_conc).flat, self.mw_met.flat))

    def _regularization(self, ln_conc: np.ndarray) -> float:
        """Calculate the regularization term.

        Regularization function:
            d      = x - 0.5 * (x_min + x_max)
            lambda = median(enzyme cost weights)
            reg    = 0.01 * lambda * 0.5 * (d.T * d)
        """
        if self.regularization is None or self.regularization.lower() == "none":
            return 0.0
        elif self.regularization.lower() == "volume":
            return self._metabolite_cost_objective(ln_conc)
        elif self.regularization.lower() == "quadratic":
            d = ln_conc - 0.5 * (ln_conc.min() + ln_conc.max())
            return self.QUAD_REGULARIZATION_COEFF * 0.5 * float(d.T * d)
        else:
            raise Exception("Unknown regularization: " + self.regularization)

    def _calc_z_scores(self, ln_conc: np.ndarray) -> np.ndarray:
        """Calculate individual zscores."""
        z_scores = np.zeros(ln_conc.shape)
        idx = self.ln_conc_sigma >= self.MINIMAL_STDEV
        z_scores[idx] = (
            ln_conc[idx] - self.ln_conc_mu[idx]
        ) / self.ln_conc_sigma[idx]
        return z_scores

    def _metabolic_adjustment_objective(self, ln_conc: np.ndarray) -> float:
        """Calculate metabolic adjustment score.

        Essentially, it is the sum of Z-scores for the multivariate Gaussian
        distribution of log-concentrations (described by mu and sigma)
        """
        return np.square(self._calc_z_scores(ln_conc)).sum()

    def optimize(
        self, ln_conc0: np.ndarray, fun: Callable[[np.ndarray], float]
    ) -> Tuple[float, np.ndarray]:
        """Optimize based on enzyme cost and metabolic adjustment (weighted sum)."""
        ln_conc0 = self._reshape_ln_conc(ln_conc0)

        if ln_conc0.size != self.Nc:
            raise ValueError(
                f"Provided initial ln_conc has wrong size: {ln_conc0.size} "
                f"instead of {self.Nc}."
            )
        if not self.is_feasible:
            raise ValueError(
                "Provided initial ln_conc is not in the feasible space."
            )

        for i in range(self.Nc):
            if ln_conc0[i] < self.ln_conc_lb[i] - self.EPSILON:
                raise ValueError(f"Provided initial ln_conc[{i}] below LB.")
            if ln_conc0[i] > self.ln_conc_ub[i] + self.EPSILON:
                raise ValueError(f"Provided initial ln_conc[{i}] above UB.")

        bounds = Bounds(
            lb=self.ln_conc_lb.squeeze(), ub=self.ln_conc_ub.squeeze()
        )
        df_lb = [  # ensure all reactions have a driving force >= 1e-3
            {"type": "ineq", "fun": lambda x: self.get_driving_forces(x) - 1e-3}
        ]

        r = minimize(fun, x0=ln_conc0, bounds=bounds, constraints=df_lb)

        if not r.success:
            raise Exception(r.message)

        return fun(r.x), r.x

    def optimize_ecm(self, ln_conc0: np.ndarray) -> Tuple[float, np.ndarray]:
        """Minimize enzyme cost.
            
        Use convex optimization to find the y with the minimal total
        enzyme cost per flux, i.e. sum(ECF(ln_conc)).
        """
        fun = lambda x: (
            self._enzyme_cost_objective(x) + self._regularization(x)
        )
        score, ln_conc_opt = self.optimize(ln_conc0, fun)
        ln_conc_opt = np.array(ln_conc_opt, ndmin=2).T
        return score, ln_conc_opt

    def pareto(self, ln_conc0: np.ndarray, steps: int = 20) -> pd.DataFrame:
        """Minimize enzyme cost versus metabolic adjustment (Pareto).

        enzyme cost is defined as in standard ECM.
        metabolic adjustment is the sum of squared Z-scores of the metabolite
        log-concentrations (relative to the prior Gaussian distribution).
        """
        data = []
        for r in np.logspace(-2, 2, steps):
            w_ec = r / (1.0 + r)
            w_ma = 1.0 - w_ec
            fun = lambda x: (
                w_ec
                * (
                    self._enzyme_cost_objective(x)
                    + self._metabolite_cost_objective(x)
                )
                + w_ma * self._metabolic_adjustment_objective(x)
            )
            score, ln_conc_opt = self.optimize(ln_conc0, fun)
            ec = self._enzyme_cost_objective(ln_conc_opt)
            ma = self._metabolic_adjustment_objective(ln_conc_opt)
            data.append((r, "obj", "enzyme_cost", None, ec))
            data.append((r, "obj", "metabolic_adjustment", None, ma))

            for j, x in enumerate(ln_conc_opt):
                data.append((r, "primal", "log_conc", j, x))
            for j, z_score in enumerate(self._calc_z_scores(ln_conc_opt)):
                data.append((r, "z_score", "log_conc", j, z_score))

            for i, df in enumerate(self.get_driving_forces(ln_conc_opt)):
                data.append((r, "primal", "driving_force", i, df))
            for i, enzyme_conc in enumerate(self.ECF(ln_conc_opt)):
                data.append((r, "primal", "enzyme_conc", i, enzyme_conc))
            for i, eta in enumerate(self._eta_thermodynamic(ln_conc_opt)):
                data.append((r, "eta", "thermodynamic", i, eta))
            for i, eta in enumerate(self._eta_kinetic(ln_conc_opt)):
                data.append((r, "eta", "kinetic", i, eta))
            for i, eta in enumerate(self._eta_allosteric(ln_conc_opt)):
                data.append((r, "eta", "allosteric", i, eta))

        return pd.DataFrame(
            data, columns=["weight", "var_type", "name", "index", "value"]
        )
