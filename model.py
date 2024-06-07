import numpy as np

class Model:
    def __init__(self): ...

    def calculate(self, *variables : float) -> float: ...

    def resolve_variables(self, expression) -> list[str]: ...

    def generate_plot_data(self, expression, xbounds : tuple[float, float], ybounds : tuple[float, float]):
        # variables = self.resolve_variables(expression)
        variables = ["x"]
        if len(variables) > 1:
            return {variables[0] : [], variables[1] : []}
        xdata = np.linspace(xbounds[0], xbounds[1], 500)
        # ydata = [y := self.calculate(x) for x in xdata if ybounds[0] < y < ybounds[1]]
        ydata = np.clip(2 * xdata * np.cos(5 * xdata), -5, 5) #fake data
        return {variables[0] : xdata, "func" : ydata}