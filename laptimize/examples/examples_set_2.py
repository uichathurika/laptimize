from laptimize.solver import Solver

'''
example_1 is from research paper
An Algorithm for Separable Non convex Programming Problems

Authors: James E. Falk and Richard M. Soland, May 1969

Non convex objective
Minimize: F(x1) = 0                   x1=0
                = -x1^2 + 4*x1 + 2    0 < x1 <= 6
                
          F(x2) = 2                   x2=0
                = -x2^2 + 2*x1 + 4    0 < x2 <= 5

convex polygon              
subject to: F1(x1, x2) = -x1 + 3*x2  <= 5
            F2(x1, x2) = 2*x1 - x2   <= 5
            F3(x1, x2) = -2*x1 + x2  <= 0
            F4(x1, x2) = x1 - 3*x2   <= 0
            0 <= x1 <= 6, 0 <= x1 <= 5  

---given solution---
solution : [x1: 0, x2: 0]
objective value :  2.0


---laptimize solution---
solution : [x1: 0, x2: 0]
objective value :  2.0

'''
example_1 = {'objective': {'x1': (lambda x: ((-(x ** 2) + 4 * x + 2) if x > 0 else (0 * x))),
                           'x2': lambda x: ((-(x ** 2) + 2 * x + 4) if x > 0 else (2 + 0 * x))},
             'constraints_1': {'x1': lambda x: 2 * x, 'x2': lambda x: -x, 'value': 5},
             'constraints_2': {'x1': lambda x: -x, 'x2': lambda x: 3 * x, 'value': 5},
             'constraints_3': {'x1': lambda x: -2 * x, 'x2': lambda x: x, 'value': 0},
             'constraints_4': {'x1': lambda x: x, 'x2': lambda x: -3 * x, 'value': 0},
             'capacity': {'x1': [0, 6], 'x2': [0, 5]}}

solution_1 = Solver(example_1, partition_len=0.5).solve()
print(solution_1)

'''
example_2 is from research paper
An Algorithm for Separable Non convex Programming Problems

Authors: James E. Falk and Richard M. Soland, May 1969

Minimize: F0(x1) = -3*(x1-0.5)^2          0 <= x1 <= 0.5
                    3*(x1-0.5)^2          0.5 <= x1 <= 1
          F0(x2) = -2*x2^2                0 <= x2 <= 2
          
subject to : F1(x1, x2) = 2*x2 - x1 <= 1
             0 <= x1 <= 1, 0 <= x1 <= 2    

---given solution---
solution : [x1: 0.799, x2: 0.899]
objective value :  -1.35


---laptimize solution---
solution : [x1: 0.75, x2: 0.875]
objective value :  -1.375
'''

example_2 = {'objective': {'x1': lambda x: (-3 * (x - 0.5) ** 2 if (0.5 >= x) and (x >= 0) else 3 * (x - 0.5) ** 2),
                           'x2': lambda x: -2 * x ** 2},
             'constraints_1': {'x1': lambda x: -x, 'x2': lambda x: 2 * x, 'value': 1},
             'capacity': {'x1': [0, 1], 'x2': [0, 2]}}

solution_2_0 = Solver(example_2, partition_len=0.5).solve()
print(solution_2_0)

solution_2_1 = Solver(example_2, partition_len=0.25).solve()
print(solution_2_1)

solution_2_2 = Solver(example_2, partition_len=0.025).solve()
print(solution_2_2)

'''
example_3 is from research paper
An Algorithm for Separable Non convex Programming Problems

Authors: James E. Falk and Richard M. Soland, May 1969

Minimize: F0(x1)     = 0             0 <= x1
                       4 - x1        x1 > 1
          F0(x2, x3) = -x2 - x3^2  

subject to : F1(x1, x2) = x2^2 -4*x1 <= 0 
             0 <= x1 <= 1, 0 <= x2 <= 2, 0 <= x3 <= 1  

---given solution---
solution : [x1: 0.0, x2: 0.0, x3: 1.0]
objective value :  -1.0


---laptimize solution---
solution : [x1: 0.0, x2: 0.0025, x3: 1.0]
objective value :  -1.0
'''

example_3 = {'objective': {'x1': lambda x: 0 if x <= 0 else (4 - x),
                           'x2': lambda x: -x,
                           'x3': lambda x: -(x) ** 2},
             'constraints_1': {'x1': lambda x: -4 * x, 'x2': lambda x: x ** 2, 'value': 0},
             'capacity': {'x1': [0, 1], 'x2': [0, 2], 'x3': [0, 1]}}

solution_3 = Solver(example_3, partition_len=0.25).solve()
print(solution_3)
