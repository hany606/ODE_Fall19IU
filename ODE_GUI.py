from tkinter import Label, Button, Entry, IntVar

class ODE_GUI:
    def __init__(self, root, gui_app_title="ODE_GUI"):
        # internal parameters
        self.update_flag = 0
        self.gui_app_geometry = "800x500"
        self.gui_app_title = gui_app_title
        self.initial_value = IntVar()
        self.steps_n = IntVar()
        self.max_X = IntVar()

        # GUI construction
        root.geometry(self.gui_app_geometry)
        root.title(self.gui_app_title)

        self.label = Label(root, text="This is our first GUI!")
        self.label.pack()

        self.label = Label(root, text="Initial Value (x0)", wraplength=50)
        self.label.place(x=15, y=400)
        self.initial_value_entry = Entry(root, textvariable=self.initial_value, width=5)
        self.initial_value_entry.place(x=10, y=450)

        self.label = Label(root, text="Steps (n)", wraplength=50)
        self.label.place(x=75, y=400)
        self.initial_value_entry = Entry(root, textvariable=self.max_X, width=5)
        self.initial_value_entry.place(x=70, y=450)

        self.label = Label(root, text="Max (X)", wraplength=50)
        self.label.place(x=135, y=400)
        self.initial_value_entry = Entry(root, textvariable=self.steps_n, width=5)
        self.initial_value_entry.place(x=130, y=450)

        self.update_button = Button(root, text="Update", command=self.update_callback)
        self.update_button.place(x=620,y=450)

        self.close_button = Button(root, text="Close", command=root.quit)
        self.close_button.place(x=720,y=450)


    def update_callback(self):
        pass
