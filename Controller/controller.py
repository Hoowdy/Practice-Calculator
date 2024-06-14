from tkinter import Tk
from View.view import View
from Model.model import Model

class Controller():
    def __init__(self):
        self.root = Tk()
        self.view = View(self.root, self)
        self.model = Model(self)

    def run(self):
        self.root.mainloop()

    def plot(self, plotter, expression : str = None):
        data, variables, stack_trace = self.model.generate_plot_data(expression, plotter.get_variables(), plotter.get_bounds())
        if expression:
            plotter.set_variables(variables)
        plotter.plot(data)
        plotter.set_output_listbox(stack_trace[0])
        plotter.set_stack_listbox(stack_trace[1])