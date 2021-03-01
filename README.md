# laptimize
laptimize is a python package to solve seperable non convex optimization problem which is based on branch and bound algorithm developed by  James E.Falk (1972) of The
George Washington University

## Installation
```sh
pip install laptimize
```

## Examples
laptimize requires Python 2.7 or Python >= 3.4

Minimize:

```sh
            F0(x1, x2) = 12x1 + 7x2 - x2^2
```


Subject to

convex polygon

            F1(x1, X2) = 2x1 + x2 - 0 <= 0            
            
non convex constraint

            F2(x1, X2) = -2x1^4 -x2 +2 <= 0
            0 <= x1 <= 2, 0 <= x1 <= 3



```sh
from laptimize.solver import Solver

example_1 = {'objective': {'x1': lambda x: 12 * x if x > 0 else 2, 'x2': lambda x: 7 * x - x ** 2},
             'constraint_1': {'x1': lambda x: -2 * (x ** 4), 'x2': lambda x: -x, 'value': -2},
             'constraint_2': {'x1': lambda x: 2 * x, 'x2': lambda x: x, 'value': 3},
             'capacity': {'x1': [0, 2], 'x2': [0, 3]}}
             
solution = Solver(example_1, partition_len=0.5).solve()
print(solution)
```
