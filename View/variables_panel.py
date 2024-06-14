from tkinter import Entry, Frame, Label, Misc, Scrollbar, StringVar, Text
from typing import Any

class VariablesPanel(Frame):
    def __init__(self, master: Misc | None = None):
        super().__init__(master)

        self._variables = {}

        self.container = Text(
            self, wrap= "char", state= "normal", borderwidth= 0, cursor= "arrow",
            yscrollcommand= self._yscroll)
        self.container.pack(fill= "both", expand= True)

        self.scroll = Scrollbar(self, command= self.container.yview)
        self.scroll.pack(side= "right", fill= "both", expand= True)

    @property
    def variables(self):
        return {key : var.get() if var.get() else key for key, var in self._variables.items()} or {}

    def _yscroll(self, *args):
        self.scroll.set(*args)

    def update_grid(self, variables : dict[str, Any]):
        self.container.configure(state= "normal")
        for key, value in variables.items():
            if key not in self._variables.keys():
                self._add_variable(key, value)
        self.container.configure(state= "disabled")

    def _add_variable(self, name : str, value : Any):
        variable_frame = Frame(self.container)
        variable_frame.pack(side= "left")
        variable_label = Label(variable_frame, text= name + "=")
        variable_label.grid(row= 0, column= 0)
        entry_variable = StringVar(variable_frame, value= str(value))
        variable_entry = Entry(variable_frame, textvariable= entry_variable, width= 10)
        variable_entry.bind("<KeyRelease>", lambda _: self.event_generate("<<VariablesPanelChange>>"))
        variable_entry.grid(row= 0, column= 1)
        self.container.window_create("end", window= variable_frame)
        self._variables[name] = entry_variable

    def clear_grid(self):
        for child in self.container.winfo_children():
            child.destroy()
        self._variables.clear()