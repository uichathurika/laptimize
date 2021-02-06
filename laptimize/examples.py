from laptimize.solver import Solver

problem = {
    'objective': {'x1': lambda x: 2 * x ** 3 - 9 * x ** 2 + 9 * x, 'x2': lambda x: -2 * x ** 3 + 9 * x ** 2 - 9 * x},
    'constraints_1': {'x1': lambda x: -6 * x ** 2, 'x2': lambda x: 18 * x, 'value': 9},
    'constraints_2': {'x1': lambda x: 6 * x ** 2, 'x2': lambda x: -18 * x, 'value': 0},
    'capacity': {'x1': [0, 3], 'x2': [0, 3]}}

problem1 = {'objective': {'x1': lambda x: -5 * x + x ** 2, 'x2': lambda x: -3 * x + x ** 2, 'value': None},
            'constraints_1': {'x1': lambda x: 2 * (x ** 4), 'x2': lambda x: x, 'value': 32},
            'constraints_2': {'x1': lambda x: x, 'x2': lambda x: 2 * (x ** 2), 'value': 32},
            'capacity': {'x1': [0, 2], 'x2': [0, 4], 'value': None}}

problem2 = {'objective': {'y1': lambda x: -2 * x ** 2, 'y2': lambda x: 2 * x ** 2, 'x0': lambda x: -2 * x + x ** 2,
                          'x1': lambda x: 2 * x ** 2, 'value': None},
            'constraints_1': {'y1': lambda x: 0, 'y2': lambda x: 0, 'x0': lambda x: x ** 3, 'x1': lambda x: -x,
                              'value': 0},
            'constraints_2': {'y1': lambda x: 0, 'y2': lambda x: 0, 'x0': lambda x: 0, 'x1': lambda x: -x, 'value': -1},
            'capacity': {'y1': [1, 505], 'y2': [-488.5, 4.5], 'x0': [1, 10], 'x1': [1, 1000], 'value': None}}

problem3 = {'objective': {'x1': lambda x: x ** 2 - 6 * x, 'x2': lambda x: x ** 2 - 8 * x, 'x3': lambda x: -0.5 * x,
                          'value': None},
            'constraints_1': {'x1': lambda x: x, 'x2': lambda x: x, 'x3': lambda x: x, 'value': 5},
            'constraints_2': {'x1': lambda x: x ** 2, 'x2': lambda x: -x, 'x3': lambda x: 0, 'value': 3},
            'capacity': {'x1': [0, 5], 'x2': [0, 5], 'x3': [0, 5], 'value': None}}

problem4 = {'objective': {'x1': (lambda x: ((-(x ** 2) + 4 * x + 2) if x > 0 else (0 * x))),
                          'x2': lambda x: ((-(x ** 2) + 2 * x + 4) if x > 0 else (2 + 0 * x)), 'value': None},
            'constraints_1': {'x1': lambda x: 2 * x, 'x2': lambda x: -x, 'value': 5},
            'constraints_2': {'x1': lambda x: -x, 'x2': lambda x: 3 * x, 'value': 5},
            'constraints_3': {'x1': lambda x: -2 * x, 'x2': lambda x: x, 'value': 0},
            'constraints_4': {'x1': lambda x: x, 'x2': lambda x: -3 * x, 'value': 0},
            'capacity': {'x1': [0, 6], 'x2': [0, 5], 'value': None}}

problem5 = {'objective': {'x1': lambda x: 12 * x, 'x2': lambda x: 7 * x - x ** 2, 'value': None},
            'constraints_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
            'constraints_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
            'capacity': {'x1': [0, 2], 'x2': [0, 3], 'value': None}}
# TODO
problem6 = {'objective': {'x1': lambda x: (-3 * (x - 0.5) ** 2 if (0.5 >= x) and (x >= 0) else 3 * (x - 0.5) ** 2),
                          'x2': lambda x: -2 * x ** 2},
            'constraints_1': {'x1': lambda x: -x, 'x2': lambda x: 2 * x, 'value': 1},
            'capacity': {'x1': [0, 1], 'x2': [0, 2]}}

adj_objective = 1
error = 0.001
values = Solver(problem6, partition_len=0.025).solve()
print(values)
