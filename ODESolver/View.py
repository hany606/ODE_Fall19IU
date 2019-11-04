from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from PIL import ImageTk, Image
from math import exp as math_exp


class View:
    def __init__(self, root, controller, x0=-4, y0=1, X=4, n=100, gui_app_title="ODE_GUI"):
        # internal parameters
        self.root = root
        self.update_flag = 0
        self.gui_app_geometry = "1000x700"
        self.gui_app_title = gui_app_title
        self.initial_value_x = DoubleVar(value=x0)
        self.initial_value_y = DoubleVar(value=y0)
        self.steps_n = DoubleVar(value=n)
        self.max_X = DoubleVar(value=X)

        self.controller = controller

        # GUI construction
        self.root.geometry(self.gui_app_geometry)
        self.root.title(self.gui_app_title)

        self.function_graph_label = Label(self.root, text="Function graph Figure")
        self.function_graph_label.place(x=170,y = 30)

        self.function_graph = Figure(figsize=(4.75, 5), dpi=100)
        # t = np.arange(0, 3, .01)
        # self.function_graph.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        self.canvas_function_graph = FigureCanvasTkAgg(self.function_graph, master=self.root)  # A tk.DrawingArea.
        self.canvas_function_graph.draw()
        self.canvas_function_graph.get_tk_widget().place(x=10,y=50)

        self.toolbar2 = NavigationToolbar2Tk(self.canvas_function_graph, self.root)
        self.toolbar2.place(x=5,y=660)
        self.canvas_function_graph.get_tk_widget().place(x=10,y=50)
        self.canvas_function_graph.mpl_connect("key_press_event", self.on_key_press)



        self.errors_label = Label(self.root, text="Errors Figure")
        self.errors_label.place(x=700,y = 30)

        self.fig_errors = Figure(figsize=(4.75, 5), dpi=100)
        # t = np.arange(0, 3, .01)
        # self.fig_errors.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        self.canvas = FigureCanvasTkAgg(self.fig_errors, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=515,y=50)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.toolbar.place(x=750,y=660)
        self.canvas.get_tk_widget().place(x=515,y=50)
        self.canvas.mpl_connect("key_press_event", self.on_key_press)


        self.label = Label(self.root, text="Initial Value (x0)", wraplength=50)
        self.label.place(x=15, y=560)
        self.initial_value_entry = Entry(self.root, textvariable=self.initial_value_x, width=5)
        self.initial_value_entry.place(x=20, y=620)

        self.label = Label(self.root, text="Initial Value (y0)", wraplength=50)
        self.label.place(x=75, y=560)
        self.initial_value_entry = Entry(self.root, textvariable=self.initial_value_y, width=5)
        self.initial_value_entry.place(x=70, y=620)

        self.label = Label(self.root, text="Steps (n)", wraplength=50)
        self.label.place(x=135, y=560)
        self.initial_value_entry = Entry(self.root, textvariable=self.steps_n, width=5)
        self.initial_value_entry.place(x=130, y=620)

        self.label = Label(self.root, text="Max (X)", wraplength=50)
        self.label.place(x=195, y=560)
        self.initial_value_entry = Entry(self.root, textvariable=self.max_X, width=5)
        self.initial_value_entry.place(x=190, y=620)

        self.update_button = Button(self.root, text="Update", command=self._update_callback)
        self.update_button.place(x=820,y=620)

        self.close_button = Button(self.root, text="Close", command=self._quit)
        self.close_button.place(x=920,y=620)


        self.label = Label(self.root, text="Equation")
        self.label.place(x=590, y=580)
        img = ImageTk.PhotoImage(Image.open("assets/equation.png"))
        panel = Label(root, image = img)
        panel.image = img
        panel.place(x=550,y=610)

        self.label = Label(self.root, text="Exact Solution")
        self.label.place(x=380, y=580)
        img = ImageTk.PhotoImage(Image.open("assets/solution.png"))
        panel = Label(root, image = img)
        panel.image = img
        panel.place(x=370,y=600)
        self.label = Label(self.root, text="Where c1 = {:}".format(((1/math_exp(x0)*y0)-1)/math_exp(x0)))
        self.label.place(x=350, y=670)
        self._update_callback()

    def on_key_press(self, event):
        # print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)
        if(event.key is "q"):
            self._quit()

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _update_callback(self):
        self.controller.set_parameters(self.initial_value_x, self.initial_value_y, self.max_X, self.steps_n)
        obj = self.controller.compute()

        self.function_graph.add_subplot(111).plot(obj["Exact"][0],obj["Exact"][1], color='green')
        self.function_graph.add_subplot(111).plot(obj["Euler"][0],obj["Euler"][1], color='red')
        # self.function_graph.add_subplot(111).plot(obj["ImprovedEuler"][0],obj["ImprovedEuler"][1], color='red')
        # self.function_graph.add_subplot(111).plot(obj["RungeKutte"][0],obj["RungeKutte"][1], color='red')
        
        
        self.canvas_function_graph.draw()

        # self.fig_errors.add_subplot(111).plot(obj.local_error.euler.x, obj.local_error.euler.y, color='green')
        # self.fig_errors.add_subplot(111).plot(obj.local_error.improved_euler.x, obj.local_error.improved_euler.y, color='red')
        # self.fig_errors.add_subplot(111).plot(obj.local_error.runge_kutta.x, obj.local_error.runge_kutta.y, color='blue')

        # self.fig_errors.add_subplot(111).plot(obj.global_error.euler.x, obj.global_error.euler.y, color='green', linestyle='dashed')
        # self.fig_errors.add_subplot(111).plot(obj.global_error.improved_euler.x, obj.global_error.improved_euler.y, color='red', linestyle='dashed')
        # self.fig_errors.add_subplot(111).plot(obj.global_error.runge_kutta.x, obj.global_error.runge_kutta.y, color='blue', linestyle='dashed')
