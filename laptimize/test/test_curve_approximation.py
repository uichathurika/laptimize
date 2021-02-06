import pytest
import pandas as pd
from laptimize.curve_approximation import CurveApproximator

problem = pd.DataFrame({'objective': {'x1': lambda x: 12*x if x > 0 else 2, 'x2':lambda x: 7*x - x**2},
                        'constraints_1': {'x1': lambda x: -2*(x**4), 'x2': lambda x: -x, 'value': -2},
                        'constraints_2': {'x1': lambda x: 2*x, 'x2': lambda x: x, 'value': 3},
                        'capacity': {'x1': [0, 2], 'x2': [0, 3]}})
x_array = [0, 1, 2, 3, 4, 5, 6]


@pytest.fixture
def curve_approximation():
    return CurveApproximator()


def test_curve_piecewise_approximation(curve_approximation):
    constraint = problem.iloc[1, :-1]
    result = curve_approximation.get_curve_approximation(constraint, x_array)
    assert len(result) == 3
    assert len(result['objective']) == len(x_array)


def test_curve_piecewise_exception(curve_approximation):
    constraint = problem.iloc[0, :-1]
    result = curve_approximation.get_curve_approximation(constraint, x_array)
    assert len(result) == 3
    assert result['objective'][0] == 2





