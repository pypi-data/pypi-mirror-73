"""thermo_models contains tools for running MDF and displaying results."""
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


import logging
from types import ModuleType
from typing import Dict, Iterable, List, Optional

import numpy as np
import optlang
import pandas as pd
from equilibrator_api import Q_, ComponentContribution, R, Reaction, default_T

from . import Bounds
from .mdf_solution import PathwayMdfSolution
from .mdmc_solution import PathwayMdmcSolution
from .pathway import Pathway
from .util import get_optlang_interface


class ThermodynamicModel(Pathway):
    """Container for doing pathway-level thermodynamic analysis."""

    def __init__(
        self,
        reactions: List[Reaction],
        fluxes: Q_,
        comp_contrib: Optional[ComponentContribution] = None,
        standard_dg_primes: Optional[np.ndarray] = None,
        dg_covariance: Optional[np.ndarray] = None,
        bounds: Optional[Bounds] = None,
        config_dict: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize a Pathway object.

        Parameters
        ----------
        reactions : List[Reaction]
            a list of Reaction objects
        fluxes : Quantity
            relative fluxes in same order as
        comp_contrib : ComponentContribution
            a ComponentContribution object
        standard_dg_primes : ndarray, optional
            reaction energies (in kJ/mol)
        dg_covariance : ndarray, optional
            square root of the uncertainty covariance matrix
            (in kJ^2/mol^2)
        bounds : Bounds, optional
            bounds on metabolite concentrations (by default uses the
            "data/cofactors.csv" file in `equilibrator-api`)
        config_dict : dict, optional
            configuration parameters for Pathway analysis
        """
        super(ThermodynamicModel, self).__init__(
            reactions=reactions,
            fluxes=fluxes,
            comp_contrib=comp_contrib,
            standard_dg_primes=standard_dg_primes,
            dg_covariance=dg_covariance,
            bounds=bounds,
            config_dict=config_dict,
        )
        self.optlang_interface = None

    def set_optlang_interface(
        self, optlang_interface: Optional[ModuleType] = None
    ) -> None:
        """Set the default optlang solver.

        Parameters
        ----------
        optlang_interface : ModuleType
            override the choice of which optlang solver to use (default: None)

        """
        self.optlang_interface = optlang_interface

    def _get_optlang_interface(self, quadratic: bool = False) -> ModuleType:
        if self.optlang_interface:
            return self.optlang_interface
        else:
            return get_optlang_interface(quadratic)

    def _make_max_min_driving_force_lp(
        self, optlang_interface: ModuleType
    ) -> optlang.Model:
        """Create primal LP problem for Min-max Thermodynamic Driving Force.

        Returns
        -------
        the linear problem object, and the three types of variables as arrays.
        """
        lp = optlang_interface.Model(name="MDF")

        # ln-concentration variables (where the units are in M before taking
        # the log)
        ln_conc = [
            optlang_interface.Variable(f"var:log_conc:{j}")
            for j in range(self.Nc)
        ]

        # the margin variable representing the MDF in units of kJ/mol
        B = optlang_interface.Variable("var:minimal_driving_force:0")

        if self.dg_sigma is not None:
            # define the ΔG'0 covariance eigenvariables
            y = [
                optlang_interface.Variable(
                    f"var:covariance_eigenvalue:{j}",
                    lb=-self.stdev_factor,
                    ub=self.stdev_factor,
                )
                for j in range(self.Nr)
            ]
        else:
            y = []

        for j in range(self.Nr):
            direction = self.I_dir[j, j]
            if direction == 0:  # an inactive reaction does not constrain ΔGs
                continue

            _rt = (R * default_T).m_as("kJ/mol")
            row = [_rt * self.S.iloc[i, j] * ln_conc[i] for i in range(self.Nc)]

            if self.dg_sigma is not None:
                # add the uncertainty value based on the covariance
                # eigenvariables (y)
                row += [
                    self.dg_sigma[j, i].m_as("kJ/mol") * y[i]
                    for i in range(self.Nr)
                ]
            if direction == 1:
                lp.add(
                    optlang_interface.Constraint(
                        sum(row) + B,
                        ub=-self.standard_dg_primes[j].m_as("kJ/mol"),
                        name=f"cnstr:driving_force:{j}",
                    )
                )
            else:
                lp.add(
                    optlang_interface.Constraint(
                        sum(row) - B,
                        lb=-self.standard_dg_primes[j].m_as("kJ/mol"),
                        name=f"cnstr:driving_force:{j}",
                    )
                )

        return lp

    def _force_concentration_bounds(
        self,
        optlang_interface: ModuleType,
        lp: optlang.Model,
        constant_only: bool = False,
    ) -> None:
        """Add lower and upper bounds for the log concentrations.
        
        Arguments
        ---------
        lp : optlang.Model
        
        constant_only : bool (optional)
            Whether to only constrain the compounds with a narrow range
            (i.e. ones with a constant concentration) or all compounds.
        """
        for j in range(self.Nc):
            if constant_only and self.ln_conc_sigma[j] > self.MINIMAL_STDEV:
                continue

            ln_conc = lp.variables.__getattr__(f"var:log_conc:{j}")
            lb = (
                self.ln_conc_mu[j]
                - self.CONFIDENCE_INTERVAL * self.ln_conc_sigma[j]
            )
            ub = (
                self.ln_conc_mu[j]
                + self.CONFIDENCE_INTERVAL * self.ln_conc_sigma[j]
            )
            lp.add(
                optlang_interface.Constraint(
                    ln_conc, lb=lb, ub=ub, name=f"cnstr:log_conc:{j}"
                )
            )

    def mdf_analysis(self) -> PathwayMdfSolution:
        """Find the MDF (Max-min Driving Force).

        Returns
        -------
        a PathwayMDFData object with the results of MDF analysis.
        """
        optlang_interface = self._get_optlang_interface(quadratic=False)
        lp_mdf = self._make_max_min_driving_force_lp(optlang_interface)
        self._force_concentration_bounds(
            optlang_interface, lp_mdf, constant_only=False
        )

        B = lp_mdf.variables.__getattr__("var:minimal_driving_force:0")
        lp_mdf.objective = optlang_interface.Objective(B, direction="max")

        if lp_mdf.optimize() != "optimal":
            logging.warning("LP status %s", lp_mdf.status)
            raise Exception("Cannot solve MDF optimization problem")

        # the MDF solution
        primal_mdf = B.primal

        # covariance eigenvalue prefactors
        primal_y = np.array(
            [
                lp_mdf.primal_values.get(f"var:covariance_eigenvalue:{j}", 0.0)
                for j in range(self.Nr)
            ],
            ndmin=2,
        ).T

        # log concentrations (excluding H2O)

        primal_lnC = np.array(
            [lp_mdf.primal_values[f"var:log_conc:{j}"] for j in range(self.Nc)],
            ndmin=2,
        ).T

        compound_prices = np.array(
            [
                lp_mdf.shadow_prices[f"cnstr:log_conc:{j}"]
                for j in range(self.Nc)
            ],
            ndmin=2,
        ).T.round(5)

        reaction_prices = np.array(
            [
                np.abs(
                    lp_mdf.shadow_prices.get(f"cnstr:driving_force:{j}", 0.0)
                )
                for j in range(self.Nr)
            ],
            ndmin=2,
        ).T.round(5)

        return PathwayMdfSolution(
            self,
            score=primal_mdf,
            ln_conc=primal_lnC,
            y=primal_y,
            reaction_prices=reaction_prices,
            compound_prices=compound_prices,
        )

    def get_zscores(self, ln_conc: Iterable) -> Iterable:
        return map(
            lambda x: (x[0] - x[1]) / x[2] if x[2] > self.MINIMAL_STDEV else 0,
            zip(ln_conc, self.ln_conc_mu, self.ln_conc_sigma),
        )

    def _add_zscore_objective(
        self, optlang_interface: ModuleType, lp: optlang.Model
    ):
        """Set the Z-score as the new objective."""
        ln_conc = map(
            lambda j: lp.variables.__getattr__(f"var:log_conc:{j}"),
            range(self.Nc),
        )
        zscores = [z ** 2 for z in self.get_zscores(ln_conc)]
        lp.objective = optlang_interface.Objective(
            sum(zscores), direction="min"
        )

    def mdmc_analysis(
        self,
        min_lb: float = 0.0,
        max_lb: Optional[float] = 10.0,
        n_steps: int = 100,
    ) -> PathwayMdmcSolution:
        """Find the MDMC (Maximum Driving-force and Metabolic Consistency.
        
        :return: a PathwayMdmcSolution object with the results of MDMC analysis.
        """
        optlang_interface = self._get_optlang_interface(quadratic=True)
        lp_mdmc = self._make_max_min_driving_force_lp(optlang_interface)
        self._force_concentration_bounds(
            optlang_interface, lp_mdmc, constant_only=True
        )
        self._add_zscore_objective(optlang_interface, lp_mdmc)

        # scan through a range of DF lower bounds to find all possible Pareto
        # optimal solutions to the bi-optimization problem (MDF and Z-score)
        B = lp_mdmc.variables.__getattr__("var:minimal_driving_force:0")
        df_constraint = optlang_interface.Constraint(
            B, lb=0, name="cnstr:minimal_driving_force:0"
        )
        lp_mdmc.add(df_constraint)

        data = []
        for lb in np.linspace(min_lb, max_lb, n_steps):
            df_constraint.lb = lb
            lp_mdmc.optimize()
            if lp_mdmc.status != "optimal":
                raise Exception("Error: LP is not optimal")
            data.append(
                (lb, "primal", "obj", "mdmc", 0, lp_mdmc.objective.value)
            )
            for value_type, value_dict in [
                ("primal", lp_mdmc.primal_values),
                ("shadow_price", lp_mdmc.shadow_prices),
                ("reduced_cost", lp_mdmc.reduced_costs),
            ]:
                for k, v in value_dict.items():
                    var_type, name, idx = k.split(":")
                    idx = int(idx)
                    data.append((lb, value_type, var_type, name, idx, v))

            # calculate the individual z-scores for log_conc variables
            ln_conc = map(
                lambda i: lp_mdmc.variables.__getattr__(
                    f"var:log_conc:{i}"
                ).primal,
                range(self.Nc),
            )
            zscores = list(self.get_zscores(ln_conc))
            for j, zscore in enumerate(zscores):
                data.append((lb, "zscore", "var", "log_conc", j, zscore))

        solution_df = pd.DataFrame(
            data=data,
            columns=[
                "df_lb",
                "value_type",
                "var_type",
                "var_name",
                "index",
                "value",
            ],
        )
        return PathwayMdmcSolution(self, solution_df)
