from tkinter import NO
from typing import Any
import numpy as np
from .calculate import Calc

class Model:
    def __init__(self, controller):
        self.controller = controller
        self.expression_manager = Calc()

    def generate_plot_data(
            self, 
            expression : str, 
            variables : dict[str, Any], 
            bounds : tuple[float, float, float, float], 
            density : int = None
        ):
        _expression, stack_trace = self.expression_manager.evaluate(expression, variables)
        _variables = self.expression_manager.variables.copy()
        unvalued_variables = [*filter(lambda k: _variables[k] == k, _variables.keys())]
        if len(unvalued_variables) > 1:
            return {"var" : [], "func" : []}, _variables, stack_trace
        xdata = np.linspace(bounds[0], bounds[1], 500)
        ydata = []
        for x in xdata:
            try:
                y, _ = self.expression_manager.evaluate(variables= {unvalued_variables[0] : x})
                if y < bounds[2]\
                or y > bounds[3]:
                    ydata.append(None)
                    continue
                ydata.append(y)
            except Exception as e:
                ydata.append(None)
                pass
        # ydata = np.clip(np.power(xdata, 2), ybounds[0], ybounds[1]) #fake data
        # ydata = np.clip(2 * xdata * np.cos(5 * xdata), ybounds[0], ybounds[1]) #fake data
        return {"var" : xdata, "func" : ydata}, _variables, stack_trace