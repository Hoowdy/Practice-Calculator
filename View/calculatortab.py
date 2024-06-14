from tkinter import Button, Entry, Frame, Label, LabelFrame, Listbox, Misc, Variable
from typing import Any
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from .variables_panel import VariablesPanel

class CalculatorTab(Frame):
    def __init__(self, master: Misc | None = None, name : str = None):
    #, cnf: dict[str, Any] | None = ..., *, background: str = ..., bd: str | float = 0, bg: str = ..., border: str | float = 0, borderwidth: str | float = 0, class_: str = "Frame", colormap: Misc | Literal['new'] | Literal[''] = "", container: bool = False, cursor: str | tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str] = "", height: str | float = 0, highlightbackground: str = ..., highlightcolor: str = ..., highlightthickness: str | float = 0, name: str = ..., padx: str | float = 0, pady: str | float = 0, relief: Literal['raised'] | Literal['sunken'] | Literal['flat'] | Literal['ridge'] | Literal['solid'] | Literal['groove'] = "flat", takefocus: bool | Callable[[str], bool | None] | Literal[0] | Literal[1] | Literal[''] = 0, visual: str | tuple[str, int] = "", width: str | float = 0) -> None:
        super().__init__(master)
        #, cnf, background=background, bd=bd, bg=bg, border=border, borderwidth=borderwidth, class_=class_, colormap=colormap, container=container, cursor=cursor, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, visual=visual, width=width)
        # self.pack(anchor= "n", fill= "both")
        self.name = name
        self.graph : Line2D = None
        self._setup_layout()
    
    def _setup_layout(self):
        self.entry_frame = Frame(self)
        self.entry_frame.place(relheight=0.15, relwidth=0.67, rely=0)
        self.entry_field = Entry(self.entry_frame, font= 10, justify= "left", background= "yellow")
        self.entry_field.pack(fill= "both", expand= True)
        # self.entry_field.bind("<KeyRelease>", lambda e: None)

        self.graph_frame = LabelFrame(self, text= "", background= "green")
        self.graph_frame.place(relheight=0.67, relwidth=0.67, rely=0.15)

        self.graph_canvas = FigureCanvasTkAgg(master= self.graph_frame)
        self.graph_canvas.get_tk_widget().pack(fill= "both", expand= True)

        if not self.graph_canvas.figure:
            self.graph_canvas.figure = Figure(
                # (self.graph_canvas.get_width_height()[0] * self.graph_canvas.device_pixel_ratio,
                # self.graph_canvas.get_width_height()[1] * self.graph_canvas.device_pixel_ratio),
                # self.graph_canvas.device_pixel_ratio
            )
        # self.graph_canvas.figure.add_subplot()
        # width, height = self.graph_canvas.get_width_height(physical= True)
        # ratio = width / height
        axes = self.graph_canvas.figure.add_axes(
            (.07, .07, .93, .93), 
            projection= "rectilinear", 
            xlim= (-5, 5), ylim= (-5, 5)
            )
        axes.set_aspect("equal")
        axes.grid(True, axis= "both")

        self.variables_panel = VariablesPanel(self)
        self.variables_panel.place(relheight=0.18, relwidth=0.67, rely=0.82)
        # self.variables_panel.update_grid(["x", "y", "z", "a", "b", "c", "d", "e"])

        # self.func_label = Label(self.func_frame, font=10, background= "red")
        # self.func_label.pack(fill= "both", expand= True)

        self.table_frame = Frame(self)
        self.table_frame.place(relheight=0.82, relwidth=0.33, relx=0.67, rely=0)

        self.output_label = Label(self.table_frame, text= "Output", font= 10)
        self.output_label.place(relheight= 0.05, relwidth= 0.5, rely=0, relx= 0)

        self.output_variable = Variable(self, [])
        self.output_column = Listbox(self.table_frame, listvariable= self.output_variable)
        self.output_column.place(relheight= 0.95, relwidth= 0.5, rely=0.05, relx= 0)
        
        self.stack_label = Label(self.table_frame, text= "Stack", font= 10)
        self.stack_label.place(relheight= 0.05, relwidth= 0.5, rely=0, relx= 0.5)

        self.stack_variable = Variable(self, [])
        self.stack_column = Listbox(self.table_frame, listvariable= self.stack_variable)
        self.stack_column.place(relheight= 0.95, relwidth= 0.5, rely=0.05, relx= 0.5)
        # self.brackets_label = Label(self.brackets_frame, font=10, background= "blue")
        # self.brackets_label.pack(fill= "both", expand= True)

        self.button_frame = Frame(self)
        self.button_frame.place(relheight=0.18, relwidth=0.33, rely=0.82, relx=0.67)

        self.brackets_button = Button(self.button_frame, text= f"Br_calc[{self.name}]")
        self.brackets_button.pack(fill= "both", expand= True)

        self.calc_button = Button(self.button_frame, text= f"Calc[{self.name}]")
        self.calc_button.pack(fill= "both", expand= True)

    @property
    def expression(self):
        return self.entry_field.get()

    def rename(self, name : str):
        self.name = name
        self.brackets_button.configure(text= f"Br_calc[{self.name}]")
        self.calc_button.configure(text= f"Calc[{self.name}]")

    def plot(self, variables : dict[str, list] = None):
        if len(variables) != 2:
            return
        axes = self.graph_canvas.figure.get_axes()[0]
        if not self.graph:
            self.graph = axes.plot(*variables.values())[0]
        else:
            self.graph.set_data(*variables.values())
        # axes.set_aspect("equal")
        self.graph_canvas.draw()
    
    def get_bounds(self):
        bbox = self.graph_canvas.figure.get_axes()[0].viewLim
        return (
            bbox.xmin, bbox.xmax,
            bbox.ymin, bbox.ymax
            )
    
    def get_variables(self):
        return self.variables_panel.variables
    
    def set_variables(self, variables : dict[str, Any]):
        self.variables_panel.clear_grid()
        self.variables_panel.update_grid(variables)
    
    def set_output_listbox(self, content : list[str]):
        self.output_variable.set(content)
    
    def set_stack_listbox(self, content : list[str]):
        self.stack_variable.set(content)