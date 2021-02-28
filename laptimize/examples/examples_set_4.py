from laptimize.solver import Solver

'''
Source : A global optimization method for non convex separable programming problems,
        European Journal of Operational Research 117 (1999) 275±292

Authors : Han-Lin Li, Chian-Son Yu

Minimize : F0(x1) = 40*x1 + 5*(|x1-10| + x1-10) - 5*(|x1-12| + x1-12)
           F0(x2) = 20*x2 - 5*(|x2-10| + x2-10) + 5*(|x2-12| + x2-12)
           F0(x3) = 30*x3 + 10*(|x3-10| + x3-10) - 5*(|x3-20| + x3-20)

subject to: F1(x1, x2, x3) = -90*x1 - 20*x2 - 40*x3 <= -2000
            F2(x1, x2, x3) = -30*x1 - 80*x2 - 60*x3 <= -1800
            F3(x1, x2, x3) = -10*x1 - 20*x2 - 60*x3 <= -1500

---given solution---
solution : ['x1': 11.04, 'x2': 12.0, 'x3': 19.16]
objective value :  1430.0


---laptimize solution---
solution : ['x1': 11.04, 'x2': 12.0, 'x3': 19.16]
objective value :  1430.0
'''

example_1 = {'objective': {'x1': lambda x: 40 * x + 5 * (abs(x - 10) + x - 10) - 5 * (abs(x - 12) + x - 12),
                           'x2': lambda x: 20 * x - 5 * (abs(x - 10) + x - 10) + 5 * (abs(x - 12) + x - 12),
                           'x3': lambda x: 30 * x + 10 * (abs(x - 10) + x - 10) - 10 * (abs(x - 20) + x - 20)},
             'constraints_1': {'x1': lambda x: -90 * x, 'x2': lambda x: -20 * x, 'x3': lambda x: -40 * x,
                               'value': -2000},
             'constraints_2': {'x1': lambda x: -30 * x, 'x2': lambda x: -80 * x, 'x3': lambda x: -60 * x,
                               'value': -1800},
             'constraints_3': {'x1': lambda x: -10 * x, 'x2': lambda x: -20 * x, 'x3': lambda x: -60 * x,
                               'value': -1500},
             'capacity': {'x1': [0, 12], 'x2': [0, 12], 'x3': [0, 20]}}

solution_1 = Solver(example_1, partition_len=0.5).solve()
print(solution_1)

'''
Source : A global optimization method for non convex separable programming problems,
        European Journal of Operational Research 117 (1999) 275±292

Authors : Han-Lin Li, Chian-Son Yu

Minimize : F0(x1) = 0.23256*(x1 - 11) + 0.00872*(|x1 - 54| + x1 - 54) - 0.04924*(|x1-142| + x1 -142)
           F0(x2) = 0.22727*(x2 -11) + 0.040475*(|x2 -55| + x2 -55) - 0.041865*(|x1-201| + x1 -201)


subject to: F1(x1, x2) = x1 + x2 = 450
            0 <= x1 <= 241, 0 <= x2 <= 250


---given solution---
solution : ['x1': 200.0, 'x2': 250.0]
objective value :  -106.0


---laptimize solution---
solution : ['x1': 200.0, 'x2': 250.0]
objective value :  -106.0
'''

example_2 = {'objective': {
    'x1': lambda x: -0.23256 * (x - 11) - 0.00872 * (abs(x - 54) + x - 54) + 0.04924 * (abs(x - 142) + x - 142),
    'x2': lambda x: -0.22727 * (x - 11) - 0.040475 * (abs(x - 55) + x - 55) + 0.041865 * (abs(x - 201) + x - 201)},
    'constraints_1': {'x1': lambda x: x, 'x2': lambda x: x, 'value': 450},
    'capacity': {'x1': [0, 241], 'x2': [0, 250]}}

solution_2 = Solver(example_2, partition_len=1).solve()
print(solution_2)
