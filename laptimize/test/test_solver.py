import pandas as pd
import pytest

from laptimize.solver import Solver

problem = pd.DataFrame({'objective': {'x1': lambda x: 12 * x if x > 0 else 2, 'x2': lambda x: 7 * x - x ** 2},
                        'constraint_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
                        'constraint_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
                        'capacity': {'x1': [0, 2], 'x2': [0, 3]}})


@pytest.fixture
def solver():
    return Solver()


def test_init(solver):
    assert solver is not None
