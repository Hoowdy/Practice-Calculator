import numpy as np

class Model:
    def __init__(self): ...

    def calculate(self) -> float: ...

    def resolve_variables(self, expression) -> list[str]: ...

    def generate_plot_data(self, expression, xbounds : tuple[float, float], ybounds : tuple[float, float]):
        # variables = self.resolve_variables(expression)
        variables = ["x"]
        if len(variables) > 1:
            return {variables[0] : [], "func" : []}
        xdata = np.linspace(xbounds[0], xbounds[1], 500)
        # ydata = [y := self.calculate(x) for x in xdata if ybounds[0] < y < ybounds[1]]
        # ydata = np.clip(np.power(xdata, 2), ybounds[0], ybounds[1]) #fake data
        ydata = np.clip(2 * xdata * np.cos(5 * xdata), ybounds[0], ybounds[1]) #fake data
        return {variables[0] : xdata, "func" : ydata}