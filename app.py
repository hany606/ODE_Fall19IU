import tkinter as tk
from ODESolver.Model import Model



root = tk.Tk()
gui = Model(root)
root.mainloop()