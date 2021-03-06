import pandas as pd
import pulp
import pytest

from laptimize.lap_model import LAPModel

problem = pd.DataFrame({'objective': {'x1': lambda x: 12 * x if x > 0 else 2, 'x2': lambda x: 7 * x - x ** 2},
                        'constraint_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
                        'constraint_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
                        'capacity': {'x1': [0, 2], 'x2': [0, 3]}})

variable_names = ['x1_0', 'x1_1', 'x1_2', 'x1_3']
x_array = [0, 1, 2, 3, 4, 5, 6]
curve = pd.DataFrame({'objective': [0, 2, 4, 6], 'constraint_1': [0, 1, 2, 3], 'constraint_2': [0, 3, 6, 9]},
                     index=variable_names)
segment = pd.DataFrame({'key': ['x1', 'x1', 'x1', 'x1'],
                        'segment': [0, 1, 2, 3]}, index=variable_names)
lp_variables = dict()
lp_variables['x1'] = pulp.LpVariable.dict('l_%s', variable_names, lowBound=0, upBound=1)

lp_variable_names = ['x1_0', 'x1_1', 'x1_2', 'x1_3', 'x1_4', 'x2_0', 'x2_1', 'x2_2', 'x2_3', 'x2_4', 'x2_5', 'x2_6']
curve_df = pd.DataFrame({'objective': [0, 2, 4, 6, 8, 0, 2, 4, 6, 8, 10, 12],
                         'constraint_1': [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6],
                         'constraint_2': [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6]}, index=lp_variable_names)
segment_df = pd.DataFrame(
    {'key': ['x1', 'x1', 'x1', 'x1', 'x1', 'x2', 'x2', 'x2', 'x2', 'x2', 'x2', 'x2'],
     'segment': [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 5, 6]}, index=lp_variable_names)


@pytest.fixture
def lap_model():
    return LAPModel()


def test_init(lap_model):
    assert lap_model is not None


def test_initialize(lap_model):
    result = lap_model.initialize(segment=segment_df, curve=curve_df, name='nlp_sub_problem')
    assert result is not None


def test_define_weights_for_segment(lap_model):
    name = 'x1'
    result = lap_model.define_weights_for_segment(variable_names, name)
    assert len(result) == len(variable_names)
    assert isinstance(result['x1_1'], pulp.LpVariable)


def test_fill_constraint_objective_arrays(lap_model):
    name = 'x1'
    lap_model.curve = curve
    lp_allocation = lap_model.define_weights_for_segment(variable_names, name)
    constraint = problem.iloc[0, :-1]
    result_1, result_2 = lap_model.fill_constraint_objective_arrays(lp_allocation, constraint)
    assert len(result_1) == len(variable_names)
    assert result_2.shape == (4, 3)


def test_add_sub_problem(lap_model):
    segment_key = 'x1'
    k = ['x1_1', 'x1_2']
    lap_model.curve = curve
    lap_model.segment = segment
    lap_model.lp_variables = lp_variables
    lap_model.add_sub_problem(segment_key, k)
    assert list(lap_model.curve.index) == k
    assert list(lap_model.segment.index) == k


def test_model_solver(lap_model):
    res1, res2, res3 = lap_model.model_solver(problem, 0.5)
    assert len(res1['x1']) == 5
    assert res1['x1']['x1_0'].value() == 0.9375
    assert res2.shape == (12, 2)
    assert res3.shape == (12, 3)


def test_global_solver(lap_model):
    segment_key = 'x1'
    k = ['x1_0', 'x1_1']
    res1, res2, res3 = lap_model.initialize(segment_df, curve_df).global_solver(segment_key, k, problem)
    assert len(res1) == 2
    assert len(res2) == 9
    assert len(res3) == 9
