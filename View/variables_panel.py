from tkinter import Entry, Frame, Label, Misc, Scrollbar, StringVar, Text

class VariablesPanel(Frame):
    def __init__(self, master: Misc | None = None):
        super().__init__(master)

        self.variables = {}

        self.container = Text(
            self, wrap= "char", state= "normal", borderwidth= 0, cursor= "arrow",
            yscrollcommand= self._yscroll)
        self.container.pack(fill= "both", expand= True)

        self.scroll = Scrollbar(self, command= self.container.yview)
        self.scroll.pack(side= "right", fill= "both", expand= True)

    def _yscroll(self, *args):
        self.scroll.set(*args)

    def update_grid(self, variables : list[str]):
        self.container.configure(state= "normal")
        for variable in variables:
            if variable not in self.variables.keys():
                self._add_variable(variable)
        self.container.configure(state= "disabled")

    def _add_variable(self, name : str):
        variable_frame = Frame(self.container)
        variable_frame.pack(side= "left")
        variable_label = Label(variable_frame, text= name + "=")
        variable_label.grid(row= 0, column= 0)
        entry_variable = StringVar(variable_frame)
        variable_entry = Entry(variable_frame, textvariable= entry_variable, width= 10)
        variable_entry.grid(row= 0, column= 1)
        self.container.window_create("end", window= variable_frame)
        self.variables[name] = entry_variable

    def clear_grid(self):
        for child in self.container.children.values():
            child.destroy()
        self.variables.clear()

    def trace_entries_change(self, func):
        for var in self.variables.values():
            var.trace_add("read", func)