from laptimize.solver import Solver

'''
Source :AN ALGORITHM FOR LOCATING APPROXIMATE GLOBAL SOLUTIONS OF NON CONVEX , SEPARABLE PROBLEMS

Author : James E. Falk, April 20 , 1972

example_1:
Minimize:   F0(x1, x2) = (2*x1^3 — 9*x1^2 + 9*x1) + (-2*x2^3 + 9*x2^2 - 9*x2)
subject to: F1(x1, x2) =  — 6x1^2 + l8x2 <= 9
            F2(x1, x2) =    6x1^2 - 18x2 <= 0
               0 <= x1, x2 <= 3

---given solution---
solution : [x1: 1.714, x2: 1.000]
objective value :  —2.857


---laptimize solution---
solution : [x1: 1.714, x2: 1.000]
objective value :  —2.857
'''

# problem definition
example_1 = {
    'objective': {'x1': lambda x: 2 * x ** 3 - 9 * x ** 2 + 9 * x, 'x2': lambda x: -2 * x ** 3 + 9 * x ** 2 - 9 * x},
    'constraints_1': {'x1': lambda x: -6 * x ** 2, 'x2': lambda x: 18 * x, 'value': 9},
    'constraints_2': {'x1': lambda x: 6 * x ** 2, 'x2': lambda x: -18 * x, 'value': 0},
    'capacity': {'x1': [0, 3], 'x2': [0, 3]}}

solution_1 = Solver(example_1, partition_len=0.25).solve()
print(solution_1)

solution_2 = Solver(example_1, partition_len=0.25).solve()
print(solution_2)

'''
Source : An Algorithm for Separable Non convex Programming Problems II - Non convex constraints

Authors: Richard M. Soland, July 1971

Minimize: F0(x1, x2) = 12*x1 + 7*x2 - x2^2
subject to : 
convex polygon
            F1(x1, X2) = 2*x1 + x2 - 3 <= 0
            0 <= x1 <= 2, 0 <= x1 <= 3
non convex constraint 
            F2(x1, X2) = -2*x1^4 -x2 +2 <=0   

---given solution---
solution : [x1: 0.0, x2: 2.0]
objective value :  10.0


---laptimize solution---
solution : [x1: 0.0, x2: 2.0]
objective value :  10.0                     

'''

example_2 = {'objective': {'x1': lambda x: 12 * x, 'x2': lambda x: 7 * x - x ** 2, 'value': None},
             'constraints_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
             'constraints_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
             'capacity': {'x1': [0, 2], 'x2': [0, 3], 'value': None}}

solution_2 = Solver(example_2, partition_len=0.5).solve()
print(solution_2)

'''
Source : http://www.universalteacherpublications.com/univ/ebooks/or/Ch15/seprablex1.htm

example_2:
Maximize:   F0(x1, x2) = 5*x1 - x1^2 + 3*x2 - x2^2

subject to :F1(x1, x2) = 2x1^4 + x2 ≤ 32
            F2(x1, x2) = x1 + 2*x2^2 ≤ 32
                    x1, x2 ≥ 0

---given solution---
solution : [x1: 1.93, x2: 1.000]
objective value :  7.9251


---laptimize solution---
solution : [x1: 1.9657142835, x2: 1.5]
objective value :  8.1986

'''

example_3 = {'objective': {'x1': lambda x: -5 * x + x ** 2, 'x2': lambda x: -3 * x + x ** 2},
             'constraints_1': {'x1': lambda x: 2 * (x ** 4), 'x2': lambda x: x, 'value': 32},
             'constraints_2': {'x1': lambda x: x, 'x2': lambda x: 2 * (x ** 2), 'value': 32},
             'capacity': {'x1': [0, 2], 'x2': [0, 4], 'value': None}}

solution_3 = Solver(example_3, partition_len=0.5).solve()
print(solution_3)

'''
Source : Nonlinear Programming, Theory and Algorithm, Second Edition

Authors : Mokhtar S. Bazaraa, Hanif D. Sherali, C. M. Shetty

Minimize : F0(x1, x2, x3) = x1^2 - 6x1 + x2^2 - 8*x2 - 0.5*x3

subject to: F1(x1, x2, x3) = x1 + x2 + x3 <= 5
            F2(x1, x2) = x1^2 - x2 <= 3
            0 <= x1, x2, x3 <= 5

---given solution---
solution : [x1: 2.0, x2: 3.0, x3: 00.0]
objective value :  23.0


---laptimize solution---
solution : [x1: 2.0, x2: 3.0, x3: 00.0]
objective value :  23.0       
'''

example_4 = {'objective': {'x1': lambda x: x ** 2 - 6 * x, 'x2': lambda x: x ** 2 - 8 * x, 'x3': lambda x: -0.5 * x,
                           'value': None},
             'constraints_1': {'x1': lambda x: x, 'x2': lambda x: x, 'x3': lambda x: x, 'value': 5},
             'constraints_2': {'x1': lambda x: x ** 2, 'x2': lambda x: -x, 'x3': lambda x: 0, 'value': 3},
             'capacity': {'x1': [0, 5], 'x2': [0, 5], 'x3': [0, 5], 'value': None}}
solution_4 = Solver(example_4, partition_len=0.025).solve()
print(solution_4)
