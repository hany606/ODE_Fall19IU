# # The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# # License: http://creativecommons.org/licenses/by-sa/3.0/	

# import matplotlib
# matplotlib.use("TkAgg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure

# import tkinter as tk
# from tkinter import ttk


# LARGE_FONT= ("Verdana", 12)


# class SeaofBTCapp(tk.Tk):

#     def __init__(self, *args, **kwargs):
        
#         tk.Tk.__init__(self, *args, **kwargs)

#         tk.Tk.iconbitmap(self, default="clienticon.ico")
#         tk.Tk.wm_title(self, "Sea of BTC client")
        
        
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand = True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.frames = {}

#         for F in (StartPage, PageOne, PageTwo, PageThree):

#             frame = F(container, self)

#             self.frames[F] = frame

#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame(StartPage)

#     def show_frame(self, cont):

#         frame = self.frames[cont]
#         frame.tkraise()

        
# class StartPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self,parent)
#         label = tk.Label(self, text="Start Page", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button = ttk.Button(self, text="Visit Page 1",
#                             command=lambda: controller.show_frame(PageOne))
#         button.pack()

#         button2 = ttk.Button(self, text="Visit Page 2",
#                             command=lambda: controller.show_frame(PageTwo))
#         button2.pack()

#         button3 = ttk.Button(self, text="Graph Page",
#                             command=lambda: controller.show_frame(PageThree))
#         button3.pack()


# class PageOne(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         button2 = ttk.Button(self, text="Page Two",
#                             command=lambda: controller.show_frame(PageTwo))
#         button2.pack()


# class PageTwo(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         button2 = ttk.Button(self, text="Page One",
#                             command=lambda: controller.show_frame(PageOne))
#         button2.pack()


# class PageThree(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button1 = ttk.Button(self, text="Back to Home",
#                             command=lambda: controller.show_frame(StartPage))
#         button1.pack()

#         f = Figure(figsize=(5,5), dpi=100)
#         a = f.add_subplot(111)
#         a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

#         canvas = FigureCanvasTkAgg(f, self)
#         canvas.show()
#         canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#         toolbar = NavigationToolbar2Tk(canvas, self)
#         toolbar.update()
#         canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        

# app = SeaofBTCapp()
# app.mainloop()
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate


button = tkinter.Button(master=root, text="Quit", command=_quit)
button.pack(side=tkinter.BOTTOM)

tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.