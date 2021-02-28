from laptimize.solver import Solver

'''
Source : On Generating Non convex Optimization Test Problems, 
         Mathematical Optimization Theory and Operations Research: 18th International Conference, page 26

Author: Maria V. Barkova

Minimize : F0(x1, x2, x3, x4) = -0.5*x1^2 + 1.5*x1 + x2 - 0.25*x3^2 + 0.75*x3 + x4 -1

subject to: F1(x1, x2) = -x1^2 - x2 <= 0
            F2(x1, X2) = (x1 -1)^2 - x2 - 2.5 <= 0
            F3(x3, X4) = -x3^2 - x4 <= 0
            F4(x3, X4) = (x3 -1)^2 - x4 - 2.5 <= 0
            
---given solution---
solution : ['x1': -0.5, 'x2': -0.25, 'x3': 1.5, 'x4': -2.25], ['x1': 0.0, 'x2': -0.75, 'x3': 1.5, 'x4': -2.25]
objective value :  -3.8125


---laptimize solution---
solution : ['x1': -0.5, 'x2': -0.25, 'x3': 1.5, 'x4': -2.25]
objective value :  -3.8125


'''
example_1 = {'objective': {'x1': lambda x: -0.5 * x ** 2 + 1.5 * x,
                           'x2': lambda x: x,
                           'x3': lambda x: -0.25 * x ** 2 + 0.75 * x,
                           'x4': lambda x: x - 1},
             'constraints_1': {'x1': lambda x: -(x) ** 2, 'x2': lambda x: -x, 'x3': lambda x: 0, 'x4': lambda x: 0,
                               'value': 0},
             'constraints_2': {'x1': lambda x: (x - 1) ** 2, 'x2': lambda x: -x, 'x3': lambda x: 0, 'x4': lambda x: 0,
                               'value': 2.5},
             'constraints_3': {'x3': lambda x: -(x) ** 2, 'x4': lambda x: -x, 'x1': lambda x: 0, 'x2': lambda x: 0,
                               'value': 0},
             'constraints_4': {'x3': lambda x: (x - 1) ** 2, 'x4': lambda x: -x, 'x1': lambda x: 0, 'x2': lambda x: 0,
                               'value': 2.5},
             'capacity': {'x1': [-2.5, 2.58], 'x2': [-2.5, 2.5], 'x3': [-2.5, 2.58], 'x4': [-2.5, 2.5]}}

solution_1 = Solver(example_1, partition_len=1).solve()
print(solution_1)

'''
Source : Nonlinear Programming Methods-Separable Programming,
         Operations Research Models and Methods

Authors : Paul A. Jensen and Jonathan F. Bard

Minimize : F0(x1, x2) = 2*x1^2 - 3*x1 + 2*x2

subject to: F1(x1, X2) = 3*x1^2 + 4*x2^2 <= 8
            F2(x1, x2) = -3*(x1-2)^2 - 5*(x2 -2)^2 <= -10
            F3(x1, x2) = 3*(x1-2)^2 + 5*(x2 -2)^2 <= 21
            0 <= x1 <= 1.75, 0 <= x1 <= 1.5
            
---given solution---
solution : ['x1': 0.9227, 'x2': 0.1282]
objective value :  -0.8089


---laptimize solution---
solution : ['x1': 0.75, 'x2': 0.086734695]
objective value :  -0.9515


'''

example_2 = {'objective': {'x1': lambda x: 2 * x ** 2 - 3 * x, 'x2': lambda x: 2 * x},
             'constraints_1': {'x1': lambda x: 3 * x ** 2, 'x2': lambda x: 4 * x ** 2, 'value': 8},
             'constraints_2': {'x1': lambda x: -3 * (x - 2) ** 2, 'x2': lambda x: -5 * (x - 2) ** 2, 'value': -10},
             'constraints_3': {'x1': lambda x: 3 * (x - 2) ** 2, 'x2': lambda x: 5 * (x - 2) ** 2, 'value': 21},
             'capacity': {'x1': [0, 1.75], 'x2': [0, 1.5], 'value': None}}

solution_2 = Solver(example_2, partition_len=0.025).solve()
print(solution_2)

'''
Source : Nonlinear Programming Methods-Separable Programming,
         Operations Research Models and Methods

Authors : Paul A. Jensen and Jonathan F. Bard

Maximize : F0(x1, x2) = 2*x1^2 - 3*x1 + 2*x2

subject to: F1(x1, X2) = 3*x1^2 + 4*x2^2 <= 8
            F2(x1, x2) = -3*(x1-2)^2 - 5*(x2 -2)^2 <= -10
            F3(x1, x2) = 3*(x1-2)^2 + 5*(x2 -2)^2 <= 21
            0 <= x1 <= 1.75, 0 <= x1 <= 1.5

---given solution---
solution : ['x1': 0.0, 'x2': 1.414]
objective value :  2.828


---laptimize solution---
solution : ['x1': 0.017694805, 'x2': 1.4140418487500002]
objective value :  2.7759


'''

example_3 = {'objective': {'x1': lambda x: -2 * x ** 2 + 3 * x, 'x2': lambda x: -2 * x},
             'constraints_1': {'x1': lambda x: 3 * x ** 2, 'x2': lambda x: 4 * x ** 2, 'value': 8},
             'constraints_2': {'x1': lambda x: -3 * (x - 2) ** 2, 'x2': lambda x: -5 * (x - 2) ** 2, 'value': -10},
             'constraints_3': {'x1': lambda x: 3 * (x - 2) ** 2, 'x2': lambda x: 5 * (x - 2) ** 2, 'value': 21},
             'capacity': {'x1': [0, 1.75], 'x2': [0, 1.5], 'value': None}}

solution_3 = Solver(example_3, partition_len=0.025).solve()
print(solution_3)
