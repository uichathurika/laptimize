import mystic.symbolic as ms
from mystic.solvers import diffev2, fmin_powell
from scipy.optimize import minimize

from laptimize.solver import Solver

problem = {
    'objective': {'x1': lambda x: 2 * x ** 3 - 9 * x ** 2 + 9 * x, 'x2': lambda x: -2 * x ** 3 + 9 * x ** 2 - 9 * x,
                  'value': None},
    'constraints_1': {'x1': lambda x: -6 * x ** 2, 'x2': lambda x: 18 * x, 'value': 9},
    'constraints_2': {'x1': lambda x: 6 * x ** 2, 'x2': lambda x: -18 * x, 'value': 0},
    'capacity': {'x1': [0, 3], 'x2': [0, 3], 'value': None}}
values = Solver(problem, partition_len=0.25).solve()
print(values)
########################################################################################################
# problem no 1
bounds = [[0, 3], [0, 3]]
func = lambda x: 2 * x[0] ** 3 - 9 * x[0] ** 2 + 9 * x[0] - 2 * x[1] ** 3 + 9 * x[1] ** 2 - 9 * x[1]
cons = ({'type': 'ineq', 'fun': lambda x: -6 * x[0] ** 2 + 18 * x[1] - 9},
        {'type': 'ineq', 'fun': lambda x: 6 * x[0] ** 2 - 18 * x[1] - 0})
res = minimize(func, (2, 1), method='SLSQP', bounds=((0, 3), (0, 3)), constraints=cons)
print(res)


####################################################################################################

def objective(x):
    return 2 * x[0] ** 3 - 9 * x[0] ** 2 + 9 * x[0] - 2 * x[1] ** 3 + 9 * x[1] ** 2 - 9 * x[1]


objective_1 = lambda x: objective(x)
equations = '''
 -6 * x0 ** 2 + 18 * x1 - 9 <= 0
 6 * x0 ** 2 - 18 * x1 - 0 <= 0
'''

bounds = [(0, 3), (0, 3)]
eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
result = diffev2(objective_1, x0=(1, 1), constraints=eqn, bounds=bounds, npop=40, ftol=1e-8, gtol=100, disp=False,
                 full_output=True)
print(result)

####################________________________############################################################################

# problem1 = {'objective': {'x1': lambda x: -5 * x + x ** 2, 'x2': lambda x: -3 * x + x ** 2, 'value': None},
#             'constraints_1': {'x1': lambda x: 2 * (x ** 4), 'x2': lambda x: x, 'value': 32},
#             'constraints_2': {'x1': lambda x: x, 'x2': lambda x: 2 * (x ** 2), 'value': 32},
#             'capacity': {'x1': [0, 2], 'x2': [0, 4], 'value': None}}
#
# values = Solver(problem1, partition_len=0.025).solve()
# print(values)
# #######################################################################################################################
# bounds = [[0, 2], [0, 4]]
# func = lambda x: -5 * x[0] + x[0] ** 2 - 3 * x[1] + x[1] ** 2
#
# cons = ({'type': 'ineq', 'fun': lambda x: 2 * (x[0] ** 4) + x[1] - 32},
#         {'type': 'ineq', 'fun': lambda x: x[0] + 2 * (x[1] ** 2) - 32})
# res = minimize(func, (0, 0), method='SLSQP', bounds=((0, 2), (0, 4)), constraints=cons);
#
# print(res)
#
#
# #######################################################################################################################
#
# def objective(x):
#     return -5 * x[0] + x[0] ** 2 - 3 * x[1] + x[1] ** 2
#
#
# objective_1 = lambda x: objective(x)
# equations = '''
#  2 * (x0 ** 4) + x1 - 32 <= 0
#  x0 + 2 * (x1 ** 2) - 32 <= 0
# '''
#
# bounds = [(0, 2), (0, 4)]
# eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
# result = diffev2(objective_1, x0=bounds, constraints=eqn, bounds=bounds, npop=40, ftol=1e-8, gtol=100, disp=False,
#                  full_output=True)
# print(result)

#######################################################################################################################
# problem6 = {'objective': {'x1': lambda x: 12 * x, 'x2': lambda x: 7 * x - x ** 2},
#             'constraints_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
#             'constraints_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
#             'capacity': {'x1': [0, 2], 'x2': [0, 3]}}
# values = Solver(problem6, partition_len=0.5).solve()
# print(values)
#
# ######################################################################################################################
# func = lambda x: 12 * x[0] + 7 * x[1] - x[1] ** 2
#
# cons = ({'type': 'ineq', 'fun': lambda x: -2 * (x[0] ** 4) - x[1] + 2},
#         {'type': 'ineq', 'fun': lambda x: 2 * x[0] + x[1] - 3})
# res = minimize(func, (0, 2), method='SLSQP', bounds=((0, 2), (0, 3)), constraints=cons);
# print(res)
#
#
# ########################################################################################################################
# def objective(x):
#     return 12 * x[0] + 7 * x[1] - x[1] ** 2
#
#
# objective_1 = lambda x: objective(x)
# equations = '''
#  -2 * (x0 ** 4) - x1 + 2 <= 0
#  2 * x0 + x1 - 3 <= 0
# '''
#
# bounds = [(0, 2), (0, 3)]
# eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
# result = diffev2(objective_1, x0=bounds, constraints=eqn, bounds=bounds, npop=40, ftol=1e-8, gtol=100, disp=False,
#                  full_output=True)
# print(result)

#######################################################################################################################
# problem3 = {'objective': {'x1': lambda x: x ** 2 - 6 * x, 'x2': lambda x: x ** 2 - 8 * x, 'x3': lambda x: -0.5 * x,
#                           'value': None},
#             'constraints_1': {'x1': lambda x: x, 'x2': lambda x: x, 'x3': lambda x: x, 'value': 5},
#             'constraints_2': {'x1': lambda x: x ** 2, 'x2': lambda x: -x, 'x3': lambda x: 0, 'value': 3},
#             'capacity': {'x1': [0, 5], 'x2': [0, 5], 'x3': [0, 5], 'value': None}}
#
# values = Solver(problem3, partition_len=0.025).solve()
# print(values)
#
# ######################################################################################################################
# func = lambda x: x[0] ** 2 - 6 * x[0] + x[1] ** 2 - 8 * x[1] - 0.5 * x[2]
#
# cons = ({'type': 'ineq', 'fun': lambda x: x[0] + x[1] + x[2] - 5},
#         {'type': 'ineq', 'fun': lambda x: x[0] ** 2 - x[1] - 3})
# res = minimize(func, (0, 0, 0), method='SLSQP', bounds=((0, 5), (0, 5), (0, 5)), constraints=cons);
# print(res)
#
#
# ########################################################################################################################
# def objective(x):
#     return x[0] ** 2 - 6 * x[0] + x[1] ** 2 - 8 * x[1] - 0.5 * x[2]
#
#
# objective_1 = lambda x: objective(x)
# equations = '''
#  x0 + x1 + x2 - 5 <= 0
#  x0 ** 2- x1 - 3 <= 0
# '''
#
# bounds = [(0, 5), (0, 5), (0, 5)]
# eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
# result = diffev2(objective_1, x0=bounds, constraints=eqn, bounds=bounds, npop=40, ftol=1e-8, gtol=100, disp=False,
#                  full_output=True)
# print(result)
#

#######################################################################################################################
# problem6 = {'objective': {'x1': lambda x: (-3 * (x - 0.5) ** 2 if (0.5 >= x) and (x >= 0) else 3 * (x - 0.5) ** 2),
#                           'x2': lambda x: -2 * x ** 2},
#             'constraints_1': {'x1': lambda x: -x, 'x2': lambda x: 2 * x, 'value': 1},
#             'capacity': {'x1': [0, 1], 'x2': [0, 2]}}
#
# values = Solver(problem6, partition_len=0.025).solve()
# print(values)
#
# ######################################################################################################################
# func = lambda x: (-3 * (x[0] - 0.5) ** 2 if (0.5 >= x[0]) and (x[0] >= 0) else 3 * (x[0] - 0.5) ** 2) - 2 * x[1] ** 2
#
# cons = ({'type': 'ineq', 'fun': lambda x: -x[0] + 2 * x[1] - 1})
# res = minimize(func, (0, 0), method='SLSQP', bounds=((0, 1), (0, 2)), constraints=cons);
# print(res)
#
#
# ########################################################################################################################
# def objective(x):
#     return (-3 * (x[0] - 0.5) ** 2 if (0.5 >= x[0]) and (x[0] >= 0) else 3 * (x[0] - 0.5) ** 2) - 2 * x[1] ** 2
#
#
# objective_1 = lambda x: objective(x)
# equations = '''
# -x0 + 2 * x1 - 1 <= 0
# '''
#
# bounds = [(0, 1), (0, 2)]
# eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
# result = diffev2(objective_1, x0=bounds, constraints=eqn, bounds=bounds, npop=40, ftol=1e-8, gtol=100, disp=False,
#                  full_output=True)
# print(result)
#######################################################################################################################
problem7 = {'objective': {'x1': lambda x: -0.5 * x ** 2 + 1.5 * x,
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

values = Solver(problem7, partition_len=0.25).solve()
print(values)

######################################################################################################################
func = lambda x: -0.5 * x[0] ** 2 + 1.5 * x[0] + x[1] - 0.25 * x[2] ** 2 + 0.75 * x[2] + x[3] - 1

cons = ({'type': 'ineq', 'fun': lambda x: -(x[0]) ** 2 - x[1]},
        {'type': 'ineq', 'fun': lambda x: (x[0] - 1) ** 2 - x[1] - 2.5},
        {'type': 'ineq', 'fun': lambda x: -(x[2]) ** 2 - x[3]},
        {'type': 'ineq', 'fun': lambda x: (x[2] - 1) ** 2 - x[3] - 2.5})
res = minimize(func, (0, 0, 0, 0), method='SLSQP', bounds=((-2.5, 2.58), (-2.5, 2.5), (-2.5, 2.58), (-2.5, 2.5)),
               constraints=cons);
print(res)


########################################################################################################################
def objective(x):
    return -0.5 * x[0] ** 2 + 1.5 * x[0] + x[1] - 0.25 * x[2] ** 2 + 0.75 * x[2] + x[3] - 1


objective_1 = lambda x: objective(x)
equations = '''
-(x0) ** 2 -x1 <= 0 
(x0 - 1) ** 2 -x1 -2.5 <= 0
-(x2) ** 2 -x3 <= 0 
(x2 - 1) ** 2 -x3 -2.5 <= 0
'''

bounds = [(-2.5, 2.58), (-2.5, 2.5), (-2.5, 2.58), (-2.5, 2.5)]
eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
result = diffev2(objective_1, x0=bounds, constraints=eqn, bounds=bounds, npop=40, ftol=1e-8, gtol=100, disp=False,
                 full_output=True)
print(result)
######################################################################################################################################

problem4 = {'objective': {'x1': (lambda x: ((-(x ** 2) + 4 * x + 2) if x > 0 else (0 * x))),
                          'x2': lambda x: ((-(x ** 2) + 2 * x + 4) if x > 0 else (2 + 0 * x)), 'value': None},
            'constraints_1': {'x1': lambda x: 2 * x, 'x2': lambda x: -x, 'value': 5},
            'constraints_2': {'x1': lambda x: -x, 'x2': lambda x: 3 * x, 'value': 5},
            'constraints_3': {'x1': lambda x: -2 * x, 'x2': lambda x: x, 'value': 0},
            'constraints_4': {'x1': lambda x: x, 'x2': lambda x: -3 * x, 'value': 0},
            'capacity': {'x1': [0, 6], 'x2': [0, 5], 'value': None}}

values = Solver(problem7, partition_len=0.25).solve()
print(values)

######################################################################################################################
func = lambda x: -0.5 * x[0] ** 2 + 1.5 * x[0] + x[1] - 0.25 * x[2] ** 2 + 0.75 * x[2] + x[3] - 1

cons = ({'type': 'ineq', 'fun': lambda x: -(x[0]) ** 2 - x[1]},
        {'type': 'ineq', 'fun': lambda x: (x[0] - 1) ** 2 - x[1] - 2.5},
        {'type': 'ineq', 'fun': lambda x: -(x[2]) ** 2 - x[3]},
        {'type': 'ineq', 'fun': lambda x: (x[2] - 1) ** 2 - x[3] - 2.5})
res = minimize(func, (0, 0, 0, 0), method='SLSQP', bounds=((-2.5, 2.58), (-2.5, 2.5), (-2.5, 2.58), (-2.5, 2.5)),
               constraints=cons);
print(res)


########################################################################################################################
def objective(x):
    return -0.5 * x[0] ** 2 + 1.5 * x[0] + x[1] - 0.25 * x[2] ** 2 + 0.75 * x[2] + x[3] - 1


objective_1 = lambda x: objective(x)
equations = '''
-(x0) ** 2 -x1 <= 0 
(x0 - 1) ** 2 -x1 -2.5 <= 0
-(x2) ** 2 -x3 <= 0 
(x2 - 1) ** 2 -x3 -2.5 <= 0
'''

bounds = [(-2.5, 2.58), (-2.5, 2.5), (-2.5, 2.58), (-2.5, 2.5)]
eqn = ms.generate_constraint(ms.generate_solvers(ms.simplify(equations)))
result = diffev2(objective_1, x0=(0, 0, 0, 0), constraints=eqn, bounds=bounds, disp=False,
                 full_output=True)
print(result)
result1 = fmin_powell(objective_1, x0=(1, -2, 1, -2), bounds=bounds, constraints=eqn)
print(result1)
