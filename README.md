# laptimize - Linear Approximated Programming for Optimization
laptimize is a python package to solve separable non convex optimization problem which is based on branch and bound algorithm developed by  James E.Falk (1972) of The
George Washington University. It has been proven that it can generate global solution for large class of nonlinear programming problems in a finite number of steps.

## Installation
```sh
pip install laptimize
```

###Dependencies
laptimize requires Python >= 3.6

NumPy (>= 1.19.2)
Pandas (>= 1.1.3)
PuLP (>= 2.3)




## Examples

Refer Examples directory for more examples

problem type which `laptimize` can applies

Separable linear/non-linear convex/non-convex minimization objective function

Minimize:


            F0(x1, x2) = 12x1 + 7x2 - x2^2


Subject to separable linear/non-linear convex/non-convex constraint with '<=' inequality

convex polygon

            F1(x1, X2) = 2x1 + x2 - 0 <= 0            
            
non convex constraint

            F2(x1, X2) = -2x1^4 -x2 +2 <= 0
            0 <= x1 <= 2, 0 <= x1 <= 3  
            
**Example Code**

    from laptimize.solver import Solver

    example_1 = {'objective': {'x1': lambda x: 12 * x, 'x2': lambda x: 7 * x - x ** 2},
             'constraint_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
             'constraint_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
             'capacity': {'x1': [0, 2], 'x2': [0, 3]}}

        
    solution = Solver(example_1, partition_len=0.5).solve()
    print(solution)
        
**Comments, bug reports, patches and suggestions are welcome.**

* Comments and suggestions: https://github.com/uichathurika/laptimize/discussions
* Bug reports: https://github.com/uichathurika/laptimize/issues
* Patches: https://github.com/uichathurika/laptimize/pulls