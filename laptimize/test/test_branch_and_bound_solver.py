import pytest
import pandas
import numpy
from laptimize.branch_and_bound_solver import BranchAndBoundSolver

error = 0.001


@pytest.fixture
def branch_and_bound_solver():
    return BranchAndBoundSolver(error)


def test_init(branch_and_bound_solver):
    assert branch_and_bound_solver is not None


