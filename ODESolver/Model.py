from . import Controller
from . import View
from sympy import symbols, exp


class Model():
    def __init__(self, root, x0=-4, y0=1, X=4, n=100):
        x, c1 = symbols("x c1")
        self.function = 1/(exp(x)*(1+(c1*exp(x))))
        print(self.function)
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.n = n
        self.controller = Controller.Controller(self.function, x0, y0, X, n)
        self.view = View.View(root, self.controller)
    
        