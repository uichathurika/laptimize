import pandas as pd

from laptimize.branch_and_bound_solver import BranchAndBoundSolver
from laptimize.lap_model import LAPModel
from laptimize.log import LogFactory


class Solver:
    """This class does solving non linear optimization problems using piecewise linear approximated programming
    branch and bond technique"""

    def __init__(self, constraints, partition_len=0.25, error=0.001):
        self.logger = LogFactory.get_logger()
        self.constraints = pd.DataFrame(constraints)
        self.error = error
        self.partition_len = partition_len
        self.lap_model = LAPModel()
        self.branch_and_bound_solver = BranchAndBoundSolver(self.error)

    def solve(self):
        """
        solve the piecewise linear lp problems and create sub lp problems using branch and bond technique

        Parameter
        --------
        constraints : dict
            have all the problem related information
            ex:  {'objective':{'x1':lambda x: 12*x,'x2':lambda x: 7*x - x**2,'value':None},
                  'constraints_1': {'x1':lambda x:-2*(x**4), 'x2':lambda x: -x ,'value':-2},
                  'constraints_2': {'x1':lambda x: 2*x, 'x2':lambda x: x ,'value' :3},
                  'capacity': {'x1':[0,2], 'x2':[0,3],'value':None}}

        Returns
        -------
        lp_intervals : dict
            Approximated solution for decision variables
            ex: {'x1':2.0,'X2':1.746}
        """
        try:
            self.constraints = self.constraints.fillna(0)
            solution_df = pd.DataFrame()
            piecewise_lp, segment, curve = self.lap_model.model_solver(self.constraints, self.partition_len)
            segment_0 = segment.copy()
            # create a combined dictionary with including segment and curve dictionaries.
            combine_segment_curve = pd.concat([segment, curve], axis=1)
            lb0, ub0, k, k_lower, k_upper, segment_key = BranchAndBoundSolver(self.error).create_subproblems(
                piecewise_lp, combine_segment_curve, self.constraints)
            solution_df = solution_df.append({'iteration_no': 0, 'sub_problem_no': 0, 'piecewise_lp': piecewise_lp,
                                              'segment': segment, 'curve': curve,
                                              'lb': lb0, 'ub': ub0, 'k': k, 'k_lower': k_lower, 'k_upper': k_upper,
                                              'branching_node': segment_key}, ignore_index=True)
            global_df = pd.DataFrame()
            while (len(solution_df)) > 0 and (len(solution_df) <= 100):
                solution_df, global_df = self.sub_problem_solve(solution_df, combine_segment_curve, global_df)
            global_solution = global_df
            global_solution['solution'] = pd.Series((dict() for i in range(len(global_solution))),
                                                    index=global_solution.index)
            global_solution = global_df.sort_values(['lb']).reset_index(drop=True)
            self.constraints = self.constraints.drop(['capacity'], axis=1)
            self.constraints = self.constraints.drop(['value'], axis=0)
            for index, row in global_solution.iterrows():
                lap_intervals = self.final_solution(row.piecewise_lp, segment_0)
                global_solution.at[index, 'solution'] = lap_intervals
            lap_intervals = global_solution.solution[0]
            lap_intervals['obj_value'] = global_solution.lb[0]
            return lap_intervals
        except Exception as err:
            self.logger.info('solve method ended with error ')
            self.logger.error(str(err))
            raise

    def sub_problem_solve(self, solution_df, combine_segment_curve, global_df):
        """
        create and solve all the sub problems for each branching nodes

        Parameter
        --------
        solution_df: pandas data frame
            includes all the details related to the sub problems solutions
        constraints: pandas data frame
            problem definition
        combine_segment_curve: pandas data frame
            all piece wise linear segments and respective function values
        global_df: pandas data frame
            includes all the local and global solutions

        Returns
        -------
        solution_df: pandas data frame
            updated solution_df
        global_df: pandas data frame
            updated global_df
        """
        iteration_no = 1
        for index, node in solution_df.iterrows():
            if (node.ub - node.lb) > self.error:
                branches = [node.k, node.k_lower, node.k_upper]
                sub_problem_no = 1
                for branch in branches:
                    if len(branch) >= 2:
                        piecewise_lp1, segment1, curve1 = self.lap_model.initialize(
                            segment=node.segment,
                            curve=node.curve).global_solver(node.branching_node, branch, self.constraints)
                        lb1, ub1, k1, k_lower1, k_upper1, segment_key1 = BranchAndBoundSolver(
                            self.error).create_subproblems(
                            piecewise_lp1, combine_segment_curve, self.constraints)

                        if (node.lb < ub1 <= node.ub) | (node.lb <= lb1 < node.ub):
                            ub1 = min(node.ub, ub1)
                            lb1 = max(node.lb, lb1)

                            solution_df = solution_df.append(
                                {'iteration_no': iteration_no, 'sub_problem_no': sub_problem_no,
                                 'piecewise_lp': piecewise_lp1,
                                 'segment': segment1, 'curve': curve1,
                                 'lb': lb1, 'ub': ub1, 'k': k1, 'k_lower': k_lower1, 'k_upper': k_upper1,
                                 'branching_node': segment_key1}, ignore_index=True)
                        sub_problem_no += 1
                iteration_no += 1
            else:
                global_df = global_df.append(node, ignore_index=True)
            solution_df.drop([index], inplace=True)
        solution_df = solution_df.reset_index(drop=True)
        return solution_df, global_df

    def final_solution(self, piecewise_lp, segment):
        """
        calculate the final solutions for the decision variables using  piecewise linear variables

        Parameters
        ----------
        piecewise_lp: dict
            final lp solution
        constraints: pandas data frame
            problem definition
        segment: pandas data frame
            piecewise linear segments

        Return
        ------
        lap_value: dict
            linear approximated solution for decision variables
        """
        try:
            lap_value = dict()
            for _, lp_constraint in self.constraints.iterrows():
                var_value = 0
                lp_allocation = piecewise_lp[lp_constraint.name]
                for key in lp_allocation:
                    try:
                        var_value = var_value + segment.loc[key].segment * lp_allocation[key].value()
                    except:
                        var_value = var_value + segment.loc[key].segment * lp_allocation[key]
                lap_value[lp_constraint.name] = var_value
            return lap_value
        except Exception as err:
            self.logger.info('final_solution method ended with error ')
            self.logger.error(str(err))
            raise
