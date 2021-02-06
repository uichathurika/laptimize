import numpy as np
from laptimize.log import LogFactory


class BranchAndBoundSolver:
    """Create branching node and sub problems """

    def __init__(self, error):
        self.logger = LogFactory.get_logger()
        '''Initialising the parameters'''
        self.error = error
        self._lower_bound = 0
        self._upper_bound = np.Infinity
        self._constraint = dict()
        self._constraint_status = []
        self._objective_initial = []
        self._objective_updated = []
        self._k_upper = []
        self._k_lower = []
        self._k = []
        self._segment_key = 0

    def create_subproblems(self, lp_variables, combine_segment_curve, constraints):
        """
        create sub problems with branching nodes

        Parameters
        ----------
        lp_variables: dict
            linear problem solution
        lp_slack: dict
            linear problem slack variable
        combine_segment_curve: pandas data frame
            piece wise linear segments and corresponding function values for objective and constraints
        constraints: pandas data frame
            problem data frame

        Returns
        -------
        segment key: string
            the branching node
        lower_bound: float
            lower bound for branching problem
        upper_bound: float
             upper bound for branching problem
        k, k_lower, k_upper: list
            new branching sub segments
        """
        try:
            # split as two dictionaries from the combined dictionary.
            constraints = constraints.drop(['capacity'], axis=1)
            values = constraints.loc['value'][1:]

            for contnt in values.index:
                self._constraint[contnt] = 0

            constraints = constraints.drop(['value'], axis=0)
            for _, lp_constraint in constraints.iterrows():
                if lp_variables.get(lp_constraint.name) is None:
                    continue

                lp_allocation = lp_variables[lp_constraint.name]
                # checking for non adjacent lambdas
                keys = list(lp_allocation.keys())
                key_len = len(keys)
                expressions = []

                expressions = self.get_weight_sum(key_len, expressions, lp_allocation, keys)
                expressions = np.array(expressions)

                # checking whether lambdas are adjacent
                if len(expressions[expressions >= 1 - self.error]) >= 1:
                    self.get_objective_adjacent(lp_allocation, lp_constraint, combine_segment_curve)
                else:
                    self.get_objective_nonadjacent(lp_allocation, lp_constraint, combine_segment_curve)

            self._lower_bound = round(sum(self._objective_initial),4)
            upper_bound = round(sum(self._objective_updated),4)
            for inequality in values.index:
                self._constraint_status.append(self._constraint[inequality] - values[inequality] < self.error)

            if False not in self._constraint_status:
                self._upper_bound = upper_bound

            return self._lower_bound, self._upper_bound, self._k, self._k_lower, self._k_upper, self._segment_key
        except Exception as err:
            self.logger.info('subproblem_solve method ended with error ')
            self.logger.error(str(err))
            raise

    def get_weight_sum(self, key_len, expressions, lp_allocation, keys):
        """
        get weight variable sum to identify adjacent weights variables

        Parameters
        ----------
        key_len: int
            piece wise variable length
        expressions: list
            empty list
        lp_allocation: list
            lp problem solution
        keys:
            linear weight variables keys

        Returns
        -------
        expressions: list
            sum of adjacent weight variables
        """
        try:
            # getting sum of adjacent weight variables
            for index in range(key_len):
                if index < key_len - 1:
                    expressions.append(lp_allocation[keys[index]].value() + lp_allocation[keys[index + 1]].value())
            return expressions

        except Exception as err:
            self.logger.info('get_adjacent_sum method ended with error ')
            self.logger.error(str(err))
            raise

    def get_objective_adjacent(self, lp_allocation, lp_constraint, combine_segment_curve):
        try:
            for key in lp_allocation:
                self._objective_initial.append(lp_allocation[key].value() * combine_segment_curve.loc[key]['objective'])
                self._objective_updated.append(lp_allocation[key].value() * combine_segment_curve.loc[key]['objective'])

            constraint_values = combine_segment_curve.iloc[:,3:]
            for constraint in constraint_values.columns:
                for key in lp_allocation:
                    self._constraint[constraint] += (lp_allocation[key].value() * combine_segment_curve.loc[key][constraint])

        except Exception as err:
            self.logger.info('get_objective_adjacent method ended with error ')
            self.logger.error(str(err))
            raise

    def get_objective_nonadjacent(self, lp_allocation, lp_constraint, combine_segment_curve):
        try:
            var_value = 0
            # calculate no of var_value and objective
            for key in lp_allocation:
                self._objective_initial.append(
                    lp_allocation[key].value() * combine_segment_curve.loc[key]['objective'])
                var_value = var_value + combine_segment_curve['segment'][key] * lp_allocation[key].value()
            # calculate new values for lp variables and find segment upper limit and lower limit.
            segment = combine_segment_curve[combine_segment_curve.key == lp_constraint.name]['segment'].to_dict()
            lower_limit = max({v for k, v in segment.items() if v <= var_value})
            upper_limit = min({v for k, v in segment.items() if v >= var_value})

            # calculate adjacent lambdas.
            for key, _ in lp_allocation.items():
                lp_allocation[key] = 0
                if (segment[key] == lower_limit) and (segment[key] == upper_limit):
                    lp_allocation[key] = 1
                else:
                    if segment[key] == lower_limit:
                        lp_allocation[key] = (upper_limit - var_value) / (upper_limit - lower_limit)

                    if segment[key] == upper_limit:
                        lp_allocation[key] = (var_value - lower_limit) / (upper_limit - lower_limit)

                self._objective_updated.append(lp_allocation[key] * combine_segment_curve.loc[key]['objective'])
                for constraint in list(self._constraint.keys()):
                    self._constraint[constraint] += (lp_allocation[key] * combine_segment_curve.loc[key][constraint])

            self.get_branch_variables(segment,upper_limit, lower_limit)
            # segment code which have non adjacent lambdas.
            self._segment_key = lp_constraint.name

        except Exception as err:
            self.logger.info('get_objective_nonadjacent method ended with error ')
            self.logger.error(str(err))
            raise

    def get_branch_variables(self, segment, upper_limit, lower_limit):
        try:
            # gettingF branching variables.
            for key, val in segment.items():
                if val >= upper_limit:
                    self._k_upper.append(key)
                if val <= lower_limit:
                    self._k_lower.append(key)
                if (val == upper_limit) | (val == lower_limit):
                    self._k.append(key)
        except Exception as err:
            self.logger.info('get_branch_variables method ended with error ')
            self.logger.error(str(err))
            raise
