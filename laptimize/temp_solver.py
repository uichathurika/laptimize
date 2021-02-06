from laptimize.branch_and_bound_solver import BranchAndBoundSolver
from laptimize.lap_model import LAPModel
from laptimize.log import LogFactory
import pandas as pd


class Solver(object):
    """This class does solving non linear optimization problems using piecewise linear approximated programing
    branch and bond technique"""

    def __init__(self, adj_objective, error):
        self.logger = LogFactory.get_logger()
        self.error = error
        self.adj_objective = adj_objective
        self.lap_model = LAPModel()
        self.branch_and_bound_solver = BranchAndBoundSolver(self.adj_objective, self.error)

    def solve_1(self, constraints):
        """
        solve the piecewise linear lp problems and create sub lp problems using branch and bond technique
        :param constraints: (dict) have all the problem related information
                             ex:  {'objective':{'x1':lambda x: 12*x,'x2':lambda x: 7*x - x**2,'value':None},
                                    'constraints_1': {'x1':lambda x:-2*(x**4), 'x2':lambda x: -x ,'value':-2},
                                    'constraints_2': {'x1':lambda x: 2*x, 'x2':lambda x: x ,'value' :3},
                                    'capacity': {'x1':[0,2], 'x2':[0,3],'value':None}}


        :return:
        """
        try:

            piecewise_lp, lp_slack, segment, curve = self.lap_model.model_solver(constraints, self.adj_objective)

            segment_0 = segment.copy()
            curve_0 = curve.copy()

            # create a combined dictionary with including segment and curve dictionaries.
            combine_segment_curve = pd.concat([segment,curve],axis=1)

            lb0, ub0, k, k_lower, k_upper, segment_key = self.branch_and_bound_solver.initialize().create_subproblems(
                piecewise_lp, lp_slack, combine_segment_curve, constraints)

            # initializing final solution.
            piecewise_lp0 = piecewise_lp
            if len(piecewise_lp.keys()) != 0:
                iteration_len = 0
                while (ub0 - lb0) > self.error:
                    iteration_len = iteration_len + 1
                    if iteration_len >= 100:
                        piecewise_lp0 = dict()
                        break

                    if len(k_upper) >= 2:

                        piecewise_lp3, lp_slack3, segment3, curve3 = self.lap_model.initialize(lp_variables=dict(),
                                                                                       segment=segment,
                                                                                       curve=curve).global_solver(
                            segment_key, k_upper, constraints, self.adj_objective)
                        lb3, ub3, k3, k_lower3, k_upper3, segment_key3 = self.branch_and_bound_solver.initialize().create_subproblems(
                            piecewise_lp3, lp_slack3, combine_segment_curve, constraints)
                        if (lb0 < ub3 <= ub0) | (lb0 <= lb3 < ub0):
                            segment_key = segment_key3
                            segment = segment3
                            curve = curve3
                            if len(k3) > 1:
                                # bounds updating
                                ub0 = min(ub0, ub3)  # no need to get min, same as ub0=ub3
                                lb0 = max(lb0, lb3)
                                k = k3
                                k_lower = k_lower3
                                k_upper = k_upper3
                                piecewise_lp0 = piecewise_lp3
                                continue

                            if len(k3) == 0:
                                ub0 = min(ub0, ub3)
                                lb0 = max(lb0, lb3)
                                ub0, lb0 = self.update_ub0_lb0_by_error(ub0, lb0, ub3, lb3)
                                piecewise_lp0 = piecewise_lp3
                                continue

                            if len(k3) == 1:
                                ub0, lb0, piecewise_lp0 = self.update_ub0_lb0_by_minmax(ub0, lb0, ub3, lb3,
                                                                                          piecewise_lp0,
                                                                                          piecewise_lp3)
                                k_upper = []
                                k_lower = k_lower3
                                continue

                    if len(k) >= 2:
                        piecewise_lp2, lp_slack2, segment2, curve2 = self.lap_model.initialize(lp_variables=dict(),
                                                                                       segment=segment,
                                                                                       curve=curve).global_solver(
                            segment_key, k, constraints, self.adj_objective)

                        lb2, ub2, k2, k_lower2, k_upper2, segment_key2 = self.branch_and_bound_solver.initialize().create_subproblems(
                            piecewise_lp2, lp_slack2, combine_segment_curve, constraints)
                        if (lb0 < ub2 <= ub0) | (lb0 <= lb2 < ub0):
                            segment_key = segment_key2
                            segment = segment2
                            curve = curve2
                            if len(k2) > 1:
                                ub0 = min(ub0, ub2)
                                lb0 = max(lb0, lb2)
                                k = k2
                                k_lower = k_lower2
                                k_upper = k_upper2
                                piecewise_lp0 = piecewise_lp2
                                continue

                            if len(k2) == 0:
                                ub0 = min(ub0, ub2)
                                lb0 = max(lb0, lb2)
                                ub0, lb0 = self.update_ub0_lb0_by_error(ub0, lb0, ub2, lb2)
                                piecewise_lp0 = piecewise_lp2
                                continue

                            if len(k2) == 1:
                                ub0, lb0, piecewise_lp0 = self.update_ub0_lb0_by_minmax(ub0, lb0, ub2, lb2,
                                                                                          piecewise_lp0,
                                                                                          piecewise_lp2)
                                K = []
                                k_upper = k_upper2
                                k_lower = k_lower2
                                continue

                    if len(k_lower) >= 2:
                        piecewise_lp1, lp_slack1, segment1, curve1 = self.lap_model.initialize(lp_variables=dict(),
                                                                                       segment=segment,
                                                                                       curve=curve).global_solver(
                            segment_key, k_lower, constraints, self.adj_objective)
                        lb1, ub1, k1, k_lower1, k_upper1, segment_key1 = self.branch_and_bound_solver.initialize().create_subproblems(
                            piecewise_lp1, lp_slack1, combine_segment_curve, constraints)

                        if (lb0 < ub1 <= ub0) | (lb0 <= lb1 < ub0):
                            segment_key = segment_key1
                            segment = segment1
                            curve = curve1
                            if len(k1) > 1:
                                ub0 = min(ub0, ub1)
                                lb0 = max(lb0, lb1)
                                K = k1
                                k_lower = k_lower1
                                k_upper = k_upper1
                                piecewise_lp0 = piecewise_lp1
                                continue
                            if len(k1) == 0:
                                ub0 = min(ub0, ub1)
                                lb0 = max(lb0, lb1)
                                ub0, lb0 = self.update_ub0_lb0_by_error(ub0, lb0, ub1, lb1)
                                piecewise_lp0 = piecewise_lp1
                                continue
                            if len(k1) == 1:
                                ub0, lb0, piecewise_lp0 = self.update_ub0_lb0_by_minmax(ub0, lb0, ub1, lb1,
                                                                                          piecewise_lp0,
                                                                                          piecewise_lp1)
                                k_lower = []
                                k_upper = k_upper1
                                continue

            lap_interval = self.final_solution(piecewise_lp0, constraints, segment_0, curve_0)

            return lap_interval
        except Exception as err:
            self.logger.info('solve method ended with error ')
            self.logger.error(str(err))
            raise

    def solve(self, constraints):
        """
        solve the piecewise linear lp problems and create sub lp problems using branch and bond technique
        :param constraints: (dict) have all the problem related information
                             ex:  {'objective':{'x1':lambda x: 12*x,'x2':lambda x: 7*x - x**2,'value':None},
                                    'constraints_1': {'x1':lambda x:-2*(x**4), 'x2':lambda x: -x ,'value':-2},
                                    'constraints_2': {'x1':lambda x: 2*x, 'x2':lambda x: x ,'value' :3},
                                    'capacity': {'x1':[0,2], 'x2':[0,3],'value':None}}


        :return:
        """
        try:
            solution_df = pd.DataFrame()
            piecewise_lp, lp_slack, segment, curve = self.lap_model.model_solver(constraints, self.adj_objective)
            segment_0 = segment.copy()
            curve_0 = curve.copy()
            # create a combined dictionary with including segment and curve dictionaries.
            combine_segment_curve = pd.concat([segment, curve], axis=1)
            lb0, ub0, k, k_lower, k_upper, segment_key = self.branch_and_bound_solver.initialize().create_subproblems(
                piecewise_lp, lp_slack, combine_segment_curve, constraints)
            solution_df = solution_df.append({'iteration_no':0,'sub_problem_no':0,'piecewise_lp': piecewise_lp,
                                              'lp_slack':lp_slack, 'segment':segment, 'curve':curve,
                                              'lb':lb0, 'ub':ub0, 'k':k, 'k_lower':k_lower, 'k_upper':k_upper,
                                              'branching_node':segment_key}, ignore_index=True)
            global_df = pd.DataFrame()
            while len(solution_df) > 0:
                solution_df,global_df = self.sub_problem_solve(solution_df, constraints, combine_segment_curve, global_df)
            global_soluation = global_df.sort_values(['lb']).head(1).reset_index(drop=True)
            lap_interval = self.final_solution(global_soluation.piecewise_lp[0], constraints,segment_0, curve_0)
            return lap_interval
        except Exception as err:
            self.logger.info('solve method ended with error ')
            self.logger.error(str(err))
            raise

    def sub_problem_solve(self, solution_df, constraints, combine_segment_curve, global_df):
        iteration_no = 1
        for index, node in solution_df.iterrows():
            if (node.ub - node.lb) > self.error:
                branches = [node.k, node.k_lower, node.k_upper]
                sub_problem_no = 1
                for branch in branches:
                    if len(branch) >= 2:
                        piecewise_lp1, lp_slack1, segment1, curve1 = self.lap_model.initialize(
                            lp_variables=dict(),
                            segment=node.segment,
                            curve=node.curve).global_solver(node.branching_node, branch, constraints, self.adj_objective)
                        lb1, ub1, k1, k_lower1, k_upper1, segment_key1 = self.branch_and_bound_solver.initialize().create_subproblems(
                            piecewise_lp1, lp_slack1, combine_segment_curve, constraints)

                        if (node.lb < ub1 <= node.ub) | (node.lb <= lb1 < node.ub):
                            ub1 = min(node.ub, ub1)
                            lb1 = max(node.lb, lb1)

                        solution_df = solution_df.append(
                            {'iteration_no': iteration_no, 'sub_problem_no': sub_problem_no, 'piecewise_lp': piecewise_lp1,
                             'lp_slack': lp_slack1, 'segment': segment1, 'curve': curve1,
                             'lb': lb1, 'ub': ub1, 'k': k1, 'k_lower': k_lower1, 'k_upper': k_upper1,
                             'branching_node': segment_key1}, ignore_index=True)

                        sub_problem_no += 1
                iteration_no += 1
            else:
                global_df = global_df.append(node, ignore_index=True)
            solution_df.drop([index],inplace=True)#.reset_index(drop=True)
        solution_df = solution_df.reset_index(drop=True)
        return solution_df, global_df





    def update_ub0_lb0_by_error(self, ub0, lb0, ub, lb):
        try:
            if ub - lb <= self.error:
                ub0 = ub
                lb0 = lb
            return ub0, lb0
        except Exception as err:
            self.logger.info('update_ub0_lb0_by_error method ended with error ')
            self.logger.error(str(err))
            raise

    def update_ub0_lb0_by_minmax(self, ub0, lb0, ub, lb, piecewise_lp0, piecewise_lp):
        try:
            ub0 = min(ub0, ub)
            lb0 = max(lb0, lb)
            piecewise_lp0 = piecewise_lp
            return ub0, lb0, piecewise_lp0
        except Exception as err:
            self.logger.info('update_ub0_lb0_by_minmax method ended with error ')
            self.logger.error(str(err))
            raise

    def final_solution(self, piecewise_lp0, constraints, segment, curve):
        try:
            lap_value = dict()
            constraints = constraints.drop(['capacity'], axis=1)
            constraints = constraints.drop(['value'], axis=0)
            for _, lp_constraint in constraints.iterrows():
                days = 0
                #if piecewise_lp0.get(lp_constraint.name) is not None:
                lp_allocation = piecewise_lp0[lp_constraint.name]
                for key in lp_allocation:

                    days = days + segment.loc[key].segment * lp_allocation[key].value()
                lap_value[lp_constraint.name] = days
            return lap_value
        except Exception as err:
            self.logger.info('final_solution method ended with error ')
            self.logger.error(str(err))
            raise
