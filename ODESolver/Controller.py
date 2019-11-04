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
        print("c1",self.c1)

    def compute(self):
        self.x = [i for i in np.arange(self.x0, self.X, ((self.X-self.x0))/self.n)]
        x, c1 = symbols("x c1")
        for i in self.x:
            evaluated_value = (self.function.subs(x,i).subs(c1, self.c1))
            print(evaluated_value)
            self.y.append(float(evaluated_value))

    def get_result(self):
        return [self.x,self.y]

class NumericalMethod:
    def __init__(self, function, x0, y0, X, n):
        self.x = []
        self.y = []
        self.function = function
        self.n = n
        self.x0 = x0
        self.X = X
        self.global_error = GlobalError(self.function, self.y, x0, y0, X, n)
        self.local_error = LocalError(self.function, self.y,  x0, y0, X, n, self.global_error)
    
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


class Euler(NumericalMethod):
    def compute(self):
        super().compute()
        h = (self.X - self.x0)/self.n
        for i in range(self.n):
            # self.function
            pass

class ImprovedEuler(NumericalMethod):
    def compute(self):
        super().compute()
        pass

class RungeKutte(NumericalMethod):
    def compute(self):
        super().compute()
        pass


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


class LocalError(Error):
    def __init__(self, function, approx_function,  x0, y0, X, n, global_error):
        super().__init__(function, approx_function, x0, y0, X, n)
        self.global_error = global_error
    
    def compute(self):
        self.x = self.global_error.x
        for i in range(self.n-1):
            self.y.append(self.global_error[i+1] - self.global_error[i])
            
class GlobalError(Error):
    def compute(self):
        self.x = [i for i in np.arange(self.x0, self.X, ((self.X-self.x0))/self.n)]
        for i in range(self.n-1):
            self.y[i].append(self.function[i] - self.approx_function[i])

class Graph:
    def __init__(self, function, x0, y0, X, n):
        self.exact_solution = Exact(function, x0, y0, X, n)
        self.y_exact_solution = self.exact_solution.get_result()[1]
        self.euler = Euler(self.y_exact_solution, x0, y0, X, n)
        self.improved_euler = ImprovedEuler(self.y_exact_solution, x0, y0, X, n)
        self.runge_kutte = RungeKutte(self.y_exact_solution, x0, y0, X, n)


class Controller:
    def __init__(self, function, x0, y0, X, n):
        self.graph = Graph(function, x0, y0, X, n)
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n
        # print(x0, y0, X, n)
    
    def compute(self):
        self.graph.exact_solution.compute()
        # self.graph.euler.compute()
        # self.graph.improved_euler.compute()
        # self.graph.runge_kutte.compute()
        return {"Exact":self.graph.exact_solution.get_result(), "Euler": self.graph.euler.get_result(), "ImprovedEuler": self.graph.improved_euler.get_result(), "RungeKutte":self.graph.runge_kutte.get_result()}

    def set_parameters(self,x0, y0, X, n):
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n