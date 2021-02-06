import numpy as np
import pandas as pd
import pulp

from laptimize.curve_approximation import CurveApproximator
from laptimize.log import LogFactory


class LAPModel(object):
    """solve the linear approximated LP problem and sub problems"""

    def __init__(self, name='nlp_problem'):
        self.logger = LogFactory.get_logger()
        self.lp_variables = dict()
        self.segment = pd.DataFrame()
        self.curve = pd.DataFrame()
        self.lp_slack = pulp.LpVariable.dict('p_%s', ['p1'], lowBound=0)
        self.model = pulp.LpProblem(name, pulp.LpMinimize)
        self.objective_expressions = []
        self.constraint_expression = []

    def initialize(self, segment=pd.DataFrame(), curve=pd.DataFrame(), name='nlp_sub_problem'):
        """
        initialize variables for branching sub problems

        Parameters
        ----------
        lp_variables: dict
            linear problem related variables
        segment: pandas data frame
            updated piecewise segment for decision variables
        curve: pandas data frame
            function values of objective and constraints function for each segment values
        name: string
            problem name

        Returns
        -------
        self
        """
        self.lp_variables = dict()
        self.segment = segment
        self.curve = curve
        self.model = pulp.LpProblem(name, pulp.LpMinimize)
        self.objective_expressions = []
        self.constraint_expression = []
        return self

    def generate_variable_names(self, no_of_segments, node_name):
        """
        generate weight variables names for approximated lp problem

        Parameters
        ---------
        no_of_segments: int
            no of piecewise linear segment
        node_name: string
            non-linear decision variable name

        Returns
        ------
        variable_names: list
            weight variable names
            ex:[x1_1,x1_2,x1_3]
        """
        variable_names = []
        for i in range(0, no_of_segments):
            variable_names.append("%s_%s" % (node_name, i))
        return variable_names

    def define_weights_for_segment(self, variable_names, name):
        """
        create linear problem related variables using piece wise variables

        Parameters
        ---------
        variable_names: list
            piece wise variable list
        name: string
            decision variable name

        Returns
        -------
        self.lp_variable : dict
            update lp_variable dictionary with weight linear problem variables
        """
        self.lp_variables[name] = pulp.LpVariable.dict('l_%s', variable_names, lowBound=0, upBound=1)
        return self.lp_variables[name]

    def fill_constraint_objective_arrays(self, lp_allocation, constraint):
        """
        update objective and constraints expression lists for linear problem

        Parameters
        ---------
        lp_allocation: dict
            linear problem variables
        constraint: pandas data frame
            problem data frame

        Returns
        -------
        weights: dict
            weights constraints expression
        problem_expressions: dict
            collection of objective and constraints expression
        """
        try:
            problem_expressions = pd.DataFrame()
            for index in constraint.index:
                constraint_expression = []
                weights = []
                for key in lp_allocation:
                    constraint_expression.append(lp_allocation[key] * self.curve.loc[key][index])
                    weights.append(lp_allocation[key])
                problem_expressions[index] = list(constraint_expression)
            return weights, problem_expressions
        except Exception as err:
            self.logger.info('fill_constraint_objective_arrays method ended with error ')
            self.logger.error(str(err))
            raise

    def add_sub_problem(self, segment_key, k):
        """
        add sub problem constraint related to the weight variable

        Parameters
        ----------
        segment_key: string
            branching variable key
        k: list
            branching sub variables key ex : [x1_1, x1_2]

        Returns
        -------
        self
        """
        # adding a sub problem
        for key in self.lp_variables[segment_key]:
            if key in k:
                continue
            else:
                self.model += self.lp_variables[segment_key][key] == 0
                self.segment = self.segment.drop([key])
                self.curve = self.curve.drop([key])

    def add_weights_sum_constraint_to_model(self, weights):
        self.model += sum(weights) == 1

    def add_model_constraint_and_objective(self, constraints, values):
        """
        add constraint and objective function to the pulp lp problem

        Parameters
        ----------
        constraints: pandas data frame
            problem data frame
        values: pandas series
                right side values for the constraints
        Returns
        -------
        self
        """
        try:
            # Add objective function to model.
            self.model += sum(constraints.objective) + self.lp_slack['p1']
            constraints = constraints.drop(['objective'], axis=1)
            for constraint_expression in constraints:
                self.model += (sum(constraints[constraint_expression]) + self.lp_slack['p1']) <= values[
                    constraint_expression]

        except Exception as err:
            self.logger.info('add_model_constraint_and_objective method ended with error ')
            self.logger.error(str(err))
            raise

    def solve_model(self):
        """
        problem solve method for lp problems
        """
        try:
            solver = pulp.PULP_CBC_CMD(msg=0)
            self.model.solve(solver)
        except Exception as err:
            self.logger.info('solve_model method ended with error ')
            self.logger.error(str(err))
            raise

    def model_solver(self, constraints_df, partition_len):
        """
        solve the initial lp problem with piecewise linear variables(weights)
        Parameters
        ----------
        constraints_df: pandas data frame
            which include problem related details,data frame version of problem dictionary

        Returns
        -------
        lp_variables: dict
            pulp solution for the lp weight variables
        lp_slack: dict
            value of the lp slack variable
        segment: pandas data frame
            segment values for each decision variable
        curve: pandas data frame
            function values of objective and constraints function for each segment values
        """
        try:
            constraint_values = pd.DataFrame()
            constraints = constraints_df.drop(['value'])
            # Iterate over constrains and build model.
            for _, constraint in constraints.iterrows():
                # piecewise linear segments.
                x_array = np.append(np.arange(constraint.capacity[0], constraint.capacity[1], partition_len),
                                    constraint.capacity[1])
                no_of_segments = len(x_array)
                constraint = constraint.drop(['capacity'])
                variable_names = self.generate_variable_names(no_of_segments, constraint.name)
                # lp variable.
                lp_allocation = self.define_weights_for_segment(variable_names, constraint.name)
                # segment value.
                segment = pd.DataFrame({'key': [constraint.name] * len(x_array), 'segment': x_array})

                segment.index = variable_names
                self.segment = pd.concat([self.segment, segment])
                # curve approximation for each segment.
                curve = pd.DataFrame(CurveApproximator().get_curve_approximation(constraint, x_array))
                curve.index = variable_names
                self.curve = pd.concat([self.curve, curve])

                weights, problem_values = self.fill_constraint_objective_arrays(lp_allocation, constraint)
                constraint_values = pd.concat([constraint_values, problem_values], axis=0)
                self.add_weights_sum_constraint_to_model(weights)

            self.add_model_constraint_and_objective(constraint_values, constraints_df.loc['value'])
            self.solve_model()

            return self.lp_variables, self.segment, self.curve
        except Exception as err:
            self.logger.info('model_solver method ended with error ')
            self.logger.error(str(err))
            raise

    def global_solver(self, segment_key, k, constraints_df):
        """
        solve the given sub lp problem with branching rule

        Parameters
        ----------
        segment_key: str
            branching variable key ex: x1
        k: list
            branching sub variables key ex : [x1_1, x1-2]
        constraints_df: pandas data frame
            which include problem related details,data frame version of problem dictionary

        Returns
        -------
        lp_variables: dict
            pulp solution for the lp weight variables
        lp_slack: dict
            value of the lp slack variable
        segment: pandas data frame
            segment values for each decision variable
        curve: pandas data frame
            function values of objective and constraints functions for each segment values
        """
        # Iterate over constrains and build model.
        try:
            constraint_values = pd.DataFrame()
            constraints = constraints_df.drop(['value'])
            for _, constraint in constraints.iterrows():
                constraint = constraint.drop(['capacity'])
                segment = self.segment[self.segment.key == constraint.name]['segment'].to_dict()
                variable_names = list(segment.keys())
                lp_allocation = self.define_weights_for_segment(variable_names, constraint.name)
                weights, problem_values = self.fill_constraint_objective_arrays(lp_allocation, constraint)
                constraint_values = pd.concat([constraint_values, problem_values], axis=0)
                self.add_weights_sum_constraint_to_model(weights)
            # adding sub problem
            self.add_sub_problem(segment_key, k)
            self.add_model_constraint_and_objective(constraint_values, constraints_df.loc['value'])
            self.solve_model()
            return self.lp_variables, self.segment, self.curve

        except Exception as err:
            self.logger.info('global_solver method ended with error ')
            self.logger.error(str(err))
            raise
