from laptimize.log import LogFactory
import numpy as np


class CurveApproximator(object):
    def __init__(self):
        """ Approximated function values for non linear objective and constraints"""
        self.logger = LogFactory.get_logger()

    def get_curve_approximation(self, constraint, x_array):
        """
        get function value for objective and the all the constraint equations

        Parameter
        --------
        constraint: pandas series
            lambda functions for represent the objective and constrains equations
        x_array: numpy array
            piecewise  segments for decision variable

        Returns
        -------
        curve_array: dict
            function values of objective and constraint corresponding to each piecewise segment
        """

        try:
            try:
                curve_array = dict()
                for key in constraint.index:
                    curve_array[key] = np.piecewise(x_array, x_array, [constraint[key]])
                return curve_array
            except:
                curve_array = dict()
                for key in constraint.index:
                    curve_list = []
                    for x in x_array:
                        curve_list.append(constraint[key](x))
                    curve_array[key] = curve_list
                return curve_array
        except Exception as err:
            self.logger.info('get_curve_approximation method ended with error ')
            self.logger.error(str(err))
            raise
