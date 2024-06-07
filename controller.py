from tkinter import Tk
from view import View
from model import Model

class Controller():
    def __init__(self):
        self.root = Tk()
        self.view = View(self.root, self)
        self.model = Model()

    def run(self):
        self.root.mainloop()

    def plot(self, expression, plotter):
        data = self.model.generate_plot_data(expression, *plotter.get_bounds())
        plotter.plot(data)