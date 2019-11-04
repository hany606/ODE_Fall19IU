from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from matplotlib.pyplot import legend,plot
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
        self.exact_checkbox_val = IntVar()
        self.euler_checkbox_val = IntVar()
        self.improved_euler_checkbox_val = IntVar()
        self.runge_kutte_checkbox_val = IntVar()
        self.local_global_error_checkbox_val = IntVar()

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

        self.canvas_error_graph = FigureCanvasTkAgg(self.fig_errors, master=self.root)  # A tk.DrawingArea.
        self.canvas_error_graph .draw()
        self.canvas_error_graph .get_tk_widget().place(x=515,y=50)

        self.toolbar = NavigationToolbar2Tk(self.canvas_error_graph , self.root)
        self.toolbar.update()
        self.toolbar.place(x=750,y=660)
        self.canvas_error_graph .get_tk_widget().place(x=515,y=50)
        self.canvas_error_graph .mpl_connect("key_press_event", self.on_key_press)


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



        # self.label = Label(self.root, text="Exact", wraplength=50)
        # self.label.place(x=700, y=560)
        self.initial_value_entry = Checkbutton(self.root, variable=self.exact_checkbox_val, text="Exact", command=self._update_callback)
        self.initial_value_entry.place(x=700, y=580)

        # self.label = Label(self.root, text="Euler", wraplength=50)
        # self.label.place(x=760, y=560)
        self.initial_value_entry = Checkbutton(self.root, text="Euler", variable=self.euler_checkbox_val, command=self._update_callback)
        self.initial_value_entry.place(x=760, y=580)

        # self.label = Label(self.root, text="Improved Euler", wraplength=70)
        # self.label.place(x=840, y=560)
        self.initial_value_entry = Checkbutton(self.root, text="Improved Euler", variable=self.improved_euler_checkbox_val, command=self._update_callback)
        self.initial_value_entry.place(x=830, y=580)

        # self.label = Label(self.root, text="Runge Kutte", wraplength=50)
        # self.label.place(x=920, y=560)
        self.initial_value_entry = Checkbutton(self.root, text="Runge Kutte", variable=self.runge_kutte_checkbox_val, command=self._update_callback)
        self.initial_value_entry.place(x=890, y=580)

        self.initial_value_entry = Checkbutton(self.root, text="Global", variable=self.local_global_error_checkbox_val, command=self._update_callback)
        self.initial_value_entry.place(x=930, y=580)



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
        key_press_handler(event, self.canvas_error_graph , self.toolbar)
        if(event.key is "q"):
            self._quit()

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _update_callback(self):
        # print("-***********************************")
        self.function_graph.clear()
        self.fig_errors.clear()
        self.controller.set_parameters(self.initial_value_x.get(), self.initial_value_y.get(), self.max_X.get(), self.steps_n.get())
        obj = self.controller.compute()
        # print(len(obj["Exact"][0]), len(obj["Exact"][1]))
        if(self.exact_checkbox_val.get()):
            self.function_graph.add_subplot(111).plot(obj["Function"]["Exact"][0],obj["Function"]["Exact"][1], color='green')
        
        if(self.euler_checkbox_val.get()):
            self.function_graph.add_subplot(111).plot(obj["Function"]["Euler"][0],obj["Function"]["Euler"][1], color='red')
            print(len(obj["LocalError"]["Euler"][0]),len(obj["LocalError"]["Euler"][1]))
            if(self.local_global_error_checkbox_val.get()):
                self.fig_errors.add_subplot(111).plot(obj["GlobalError"]["Euler"][0],obj["GlobalError"]["Euler"][1], color='red')
            else:
                self.fig_errors.add_subplot(111).plot(obj["LocalError"]["Euler"][0],obj["LocalError"]["Euler"][1], color='red')

        if(self.improved_euler_checkbox_val.get()):
            self.function_graph.add_subplot(111).plot(obj["Function"]["ImprovedEuler"][0],obj["Function"]["ImprovedEuler"][1], color='blue')
            if(self.local_global_error_checkbox_val.get()):
                self.fig_errors.add_subplot(111).plot(obj["GlobalError"]["ImprovedEuler"][0],obj["GlobalError"]["ImprovedEuler"][1], color='blue')
            else:
                self.fig_errors.add_subplot(111).plot(obj["LocalError"]["ImprovedEuler"][0],obj["LocalError"]["ImprovedEuler"][1], color='blue')

        if(self.runge_kutte_checkbox_val.get()):
            self.function_graph.add_subplot(111).plot(obj["Function"]["RungeKutte"][0],obj["Function"]["RungeKutte"][1], color='yellow')
            if(self.local_global_error_checkbox_val.get()):
                self.fig_errors.add_subplot(111).plot(obj["GlobalError"]["RungeKutte"][0],obj["GlobalError"]["RungeKutte"][1], color='yellow')
            else:
                self.fig_errors.add_subplot(111).plot(obj["LocalError"]["RungeKutte"][0],obj["LocalError"]["RungeKutte"][1], color='yellow')
        
        self.fig_errors.legend(handless=)        
        self.canvas_function_graph.draw()
        self.canvas_error_graph.draw()
 
        # legend(label="Line 1", linestyle='--', loc='upper right')
