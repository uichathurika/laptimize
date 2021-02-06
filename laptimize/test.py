import pandas as pd
import numpy as np
from datetime import date, timedelta
import numpy as np
import mystic as mys
from scipy.optimize import minimize
problem = {'objective':{'x1':lambda x:2*x**3 - 9*x**2 + 9*x,'x2':lambda x:-2*x**3 + 9*x**2 -9*x,'value':None},
           'constraints_1': {'x1':lambda x:-6*x**2, 'x2':lambda x:18*x,'value':9},
           'constraints_2': {'x1':lambda x:6*x**2, 'x2':lambda x:-18*x,'value' :0},
           'capacity': {'x1':[0,3], 'x2':[0,3],'value':None}}



#problem no 1
bounds=[[0,3],[0,3]]
func = lambda x:2*x[0]**3 - 9*x[0]**2 + 9*x[0]-2*x[1]**3 + 9*x[1]**2 -9*x[1]

cons = ({'type': 'ineq', 'fun': lambda x:-6*x[0]**2+18*x[1]-9},
        {'type': 'ineq', 'fun': lambda x:6*x[0]**2-18*x[1]-0})
res = minimize(func, (1,1), method='SLSQP', bounds= ((0, 3), (0, 3)), constraints = cons);





problem1 = {'objective':{'x1':lambda x: -5*x + x**2,'x2':lambda x: -3*x + x**2,'value':None},
           'constraints_1': {'x1':lambda x:2*(x**4), 'x2':lambda x:x,'value':32},
           'constraints_2': {'x1':lambda x:x, 'x2':lambda x:2*(x**2),'value' :32},
           'capacity': {'x1':[0,2], 'x2':[0,4],'value':None}}
#problem no 2
bounds=[[0,2],[0,4]]
func = lambda x:-5*x[0] + x[0]**2-3*x[1] + x[1]**2

cons = ({'type': 'ineq', 'fun': lambda x:2*(x[0]**4) + x[1]-32},
        {'type': 'ineq', 'fun': lambda x:x[0] + 2*(x[0]**2)-32})
res = minimize(func, (0,0), method='SLSQP', bounds= ((0, 2), (0, 4)), constraints = cons);




problem6 = {'objective':{'x1':lambda x: 12*x,'x2':lambda x: 7*x - x**2},
            'constraints_1': {'x1':lambda x:-2*(x**4), 'x2':lambda x: -x ,'value':-2},
            'constraints_2': {'x1':lambda x: 2*x, 'x2':lambda x: x, 'value':3},
            'capacity': {'x1':[0,2], 'x2':[0,3]}}

func = lambda x: 12*x[0] + 7*x[1] - x[1]**2

cons = ({'type': 'ineq', 'fun': lambda x: -2*(x[0]**4) - x[1] + 2},
        {'type': 'ineq', 'fun': lambda x:2*x[0] + x[1] - 3})
res = minimize(func, (0, 0), method='SLSQP', bounds=((0, 2), (0, 3)), constraints = cons);


print (res)
