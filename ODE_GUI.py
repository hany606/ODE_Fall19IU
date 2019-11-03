from tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
from PIL import ImageTk, Image


class ODE_GUI:
    def __init__(self, root, gui_app_title="ODE_GUI"):
        # internal parameters
        self.root = root
        self.update_flag = 0
        self.gui_app_geometry = "1000x700"
        self.gui_app_title = gui_app_title
        self.initial_value_x = IntVar(value=-4)
        self.initial_value_y = IntVar(value=1)
        self.steps_n = IntVar(value=100)
        self.max_X = IntVar(value=4)

        # GUI construction
        self.root.geometry(self.gui_app_geometry)
        self.root.title(self.gui_app_title)

        self.function_graph_label = Label(self.root, text="Function graph Figure")
        self.function_graph_label.place(x=170,y = 30)

        self.function_graph = Figure(figsize=(4.75, 5), dpi=100)
        t = np.arange(0, 3, .01)
        self.function_graph.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        self.canvas2 = FigureCanvasTkAgg(self.function_graph, master=self.root)  # A tk.DrawingArea.
        self.canvas2.draw()
        self.canvas2.get_tk_widget().place(x=10,y=50)

        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.root)
        self.toolbar2.place(x=5,y=660)
        self.canvas2.get_tk_widget().place(x=10,y=50)
        self.canvas2.mpl_connect("key_press_event", self.on_key_press)



        self.errors_label = Label(self.root, text="Errors Figure")
        self.errors_label.place(x=700,y = 30)

        self.fig_errors = Figure(figsize=(4.75, 5), dpi=100)
        t = np.arange(0, 3, .01)
        self.fig_errors.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

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
        self.initial_value_entry.place(x=10, y=620)

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
        self.label = Label(self.root, text="Where c1 = 2926.35983701")
        self.label.place(x=350, y=650)
        

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
        pass
