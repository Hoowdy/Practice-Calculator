from tkinter import NO
import numpy as np
from .calculate import Calc
from .prc import process_expression
from .infix_to_postfix import infix_to_postfix

class Model:
    def __init__(self, controller):
        self.controller = controller
        self.expression_manager = Calc()

    def generate_plot_data(self, expression : str, xbounds : tuple[float, float], ybounds : tuple[float, float]):
        _expression = infix_to_postfix(process_expression(expression))
        # variables = self.expression_manager.get_unvalued_variables()
        # if len(variables) > 1:
        #     return {variables[0] : [], "func" : []}
        xdata = np.linspace(xbounds[0], xbounds[1], 500)
        ydata = []
        for x in xdata:
            try:
                y = self.expression_manager.evaluate(_expression, {"x": x})
                # if ybounds[0] < y < ybounds[1]:
                #     ydata.append(None)
                #     continue
                ydata.append(y)
            except Exception:
                ydata.append(None)
                pass
        # ydata = np.clip(np.power(xdata, 2), ybounds[0], ybounds[1]) #fake data
        # ydata = np.clip(2 * xdata * np.cos(5 * xdata), ybounds[0], ybounds[1]) #fake data
        return {"x" : xdata, "func" : ydata}