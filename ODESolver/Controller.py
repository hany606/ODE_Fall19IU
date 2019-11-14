import numpy as np
from math import exp as math_exp
from sympy import symbols, exp



class Exact:
    def __init__(self, function, x0, y0, X, n):
        self.x = []
        self.y = []
        self.n = n
        self.x0 = x0
        self.X = X
        self.c1 = ((1/math_exp(x0)*y0)-1)/math_exp(x0)
        self.function = function

    def compute(self):
        self.x = [i for i in np.arange(self.x0, self.X, ((self.X-self.x0))/self.n)]
        x, c1 = symbols("x c1")
        for i in self.x:
            evaluated_value = (self.function.subs(x,i).subs(c1, self.c1))
            # print(evaluated_value)
            self.y.append(float(evaluated_value))

    def get_result(self):
        return [self.x,self.y]
    
    def clean(self):
        self.y = []
        self.x = []


class NumericalMethod:
    def __init__(self, function_dash, function, x0, y0, X, n):
        self.x = []
        self.y = []
        self.function_dash = function_dash
        self.function_exact_val = function
        self.n = n
        self.x0 = x0
        self.X = X
        self.y0 = y0
        self.global_error = GlobalError(self.function_exact_val, self.y, x0, y0, X, n)
        self.local_error = LocalError(self.function_exact_val, self.y,  x0, y0, X, n, self.global_error)
    
    def get_result(self):
        return [self.x,self.y]

    def get_local_error(self):
        return self.local_error.get_result()

    def get_global_error(self):
        return self.global_error.get_result()
        
    # The algorithm for each function
    def compute(self):
        self.global_error.compute()
        self.local_error.compute()
    
    def clean(self):
        self.y = []
        self.x = []
        self.global_error.clean()
        self.local_error.clean()

class Euler(NumericalMethod):
    def compute(self):
        self.x = [i for i in np.arange(self.x0, self.X, ((self.X-self.x0))/self.n)]
        h = (self.X - self.x0)/self.n
        self.y.append(self.y0)
        x, y = symbols("x y")
        for i in range(int(self.n)):
            evaluated_value = (self.function_dash.subs(x,self.x[i]).subs(y, self.y[i]))
            self.y.append(self.y[i] + h*(evaluated_value))
        self.y = self.y[0:-1]
        super().compute()

class ImprovedEuler(NumericalMethod):
    def compute(self):
        self.x = [i for i in np.arange(self.x0, self.X, ((self.X-self.x0))/self.n)]
        h = (self.X - self.x0)/self.n
        self.y.append(self.y0)
        x, y = symbols("x y")
        for i in range(int(self.n)):
            k1 = (self.function_dash.subs(x,self.x[i]).subs(y, self.y[i]))
            k2 = (self.function_dash.subs(x,self.x[i]+h).subs(y, self.y[i]+k1*h))
            self.y.append(self.y[i] + h/2*(k1+k2))
        self.y = self.y[0:-1]
        super().compute()

class RungeKutte(NumericalMethod):
    def compute(self):
        self.x = [i for i in np.arange(self.x0, self.X, ((self.X-self.x0))/self.n)]
        h = (self.X - self.x0)/self.n
        self.y.append(self.y0)
        x, y = symbols("x y")
        for i in range(int(self.n)):
            k1 = (self.function_dash.subs(x,self.x[i]).subs(y, self.y[i]))
            k2 = (self.function_dash.subs(x,self.x[i]+h/2).subs(y, self.y[i]+k1*h/2))
            k3 = (self.function_dash.subs(x,self.x[i]+h/2).subs(y, self.y[i]+k2*h/2))
            k4 = (self.function_dash.subs(x,self.x[i]+h).subs(y, self.y[i]+k3*h))

            self.y.append(self.y[i] + h/6*(k1+2*k2+2*k3+k4))
        self.y = self.y[0:-1]
        super().compute()


class Error:
    def __init__(self, function, approx_function, x0, y0, X, n):
        self.function = function
        self.approx_function = approx_function
        self.n = n
        self.x0 = x0
        self.X = X
        self.x = []
        self.y = []

    def get_result(self):
        return [self.x,self.y]

    # The algorithm for each function
    def compute(self):
        pass
    
    def clean(self):
        self.y = []
        self.x = []


class LocalError(Error):
    def __init__(self, function, approx_function,  x0, y0, X, n, global_error):
        super().__init__(function, approx_function, x0, y0, X, n)
        self.global_error = global_error
    
    def compute(self):
        self.x = self.global_error.x[0:-1]
        self.global_error_y = self.global_error.y
        # print(len(self.global_error_y), len(self.x))
        for i in range(int(self.n)-1):
            self.y.append(self.global_error_y[i+1] - self.global_error_y[i])
        # print(len(self.y))  
class GlobalError(Error):
    def compute(self):
        self.x = [i for i in range(int(self.n))]
        # print(self.function)
        for i in range(int(self.n)):
            # print(i)
            self.y.append(self.function[i] - self.approx_function[i])

class Graph:
    def __init__(self, function_dash, function, x0, y0, X, n):
        self.exact_solution = Exact(function, x0, y0, X, n)
        self.y_exact_solution = self.exact_solution.get_result()[1]
        self.euler = Euler(function_dash, self.y_exact_solution, x0, y0, X, n)
        self.improved_euler = ImprovedEuler(function_dash, self.y_exact_solution, x0, y0, X, n)
        self.runge_kutte = RungeKutte(function_dash, self.y_exact_solution, x0, y0, X, n)
    
    def compute(self, function_dash, function, x0, y0, X, n):
        self.exact_solution = Exact(function, x0, y0, X, n)
        self.y_exact_solution = self.exact_solution.get_result()[1]
        self.euler = Euler(function_dash, self.y_exact_solution, x0, y0, X, n)
        self.improved_euler = ImprovedEuler(function_dash, self.y_exact_solution, x0, y0, X, n)
        self.runge_kutte = RungeKutte(function_dash, self.y_exact_solution, x0, y0, X, n)
    
    def clean(self):
        self.exact_solution.clean()
        self.euler.clean()
        self.improved_euler.clean()
        self.runge_kutte.clean()


class Controller:
    def __init__(self, function_dash, function, x0, y0, X, n):
        self.graph = Graph(function_dash, function, x0, y0, X, n)
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n
        self.function = function
        self.function_dash = function_dash
        # print(x0, y0, X, n)
    
    def compute(self):
        self.graph.clean()
        self.graph.compute(self.function_dash, self.function, self.x0, self.y0, self.X, self.n)
        self.graph.exact_solution.compute()
        self.graph.euler.compute()
        self.graph.improved_euler.compute()
        self.graph.runge_kutte.compute()
        return {"Function": {"Exact":self.graph.exact_solution.get_result(), "Euler": self.graph.euler.get_result(), "ImprovedEuler": self.graph.improved_euler.get_result(), "RungeKutte":self.graph.runge_kutte.get_result()}, "LocalError": {"Euler": self.graph.euler.local_error.get_result(), "ImprovedEuler": self.graph.improved_euler.local_error.get_result(), "RungeKutte":self.graph.runge_kutte.local_error.get_result()}, "GlobalError": {"Euler": self.graph.euler.global_error.get_result(), "ImprovedEuler": self.graph.improved_euler.global_error.get_result(), "RungeKutte":self.graph.runge_kutte.global_error.get_result()}}

    def set_parameters(self,x0, y0, X, n):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n