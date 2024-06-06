from tkinter import Button, Entry, Frame, Label, Misc
from typing import Any, Literal, Callable

class CalculatorTab(Frame):
    def __init__(self, master: Misc | None = None, name : str = None):
    #, cnf: dict[str, Any] | None = ..., *, background: str = ..., bd: str | float = 0, bg: str = ..., border: str | float = 0, borderwidth: str | float = 0, class_: str = "Frame", colormap: Misc | Literal['new'] | Literal[''] = "", container: bool = False, cursor: str | tuple[str] | tuple[str, str] | tuple[str, str, str] | tuple[str, str, str, str] = "", height: str | float = 0, highlightbackground: str = ..., highlightcolor: str = ..., highlightthickness: str | float = 0, name: str = ..., padx: str | float = 0, pady: str | float = 0, relief: Literal['raised'] | Literal['sunken'] | Literal['flat'] | Literal['ridge'] | Literal['solid'] | Literal['groove'] = "flat", takefocus: bool | Callable[[str], bool | None] | Literal[0] | Literal[1] | Literal[''] = 0, visual: str | tuple[str, int] = "", width: str | float = 0) -> None:
        super().__init__(master)
        #, cnf, background=background, bd=bd, bg=bg, border=border, borderwidth=borderwidth, class_=class_, colormap=colormap, container=container, cursor=cursor, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, visual=visual, width=width)
        # self.pack(anchor= "n", fill= "both")
        self.name = name

        self.entry_frame = Frame(self)
        self.entry_frame.place(relheight=0.15, relwidth=0.67, rely=0)
        self.entry_field = Entry(self.entry_frame, font= 10, justify= "left", background= "yellow")
        self.entry_field.pack(fill= "both", expand= True)
        # self.entry_field.bind("<KeyRelease>", lambda e: None)

        self.graph = Frame(self, background= "green")
        self.graph.place(relheight=0.67, relwidth=0.67, rely=0.15)

        self.func_frame = Frame(self)
        self.func_frame.place(relheight=0.18, relwidth=0.67, rely=0.82)

        self.func_label = Label(self.func_frame, font=10, background= "red")
        self.func_label.pack(fill= "both", expand= True)

        self.brackets_frame = Frame(self)
        self.brackets_frame.place(relheight=0.82, relwidth=0.33, relx=0.67, rely=0)

        self.brackets_label = Label(self.brackets_frame, font=10, background= "blue")
        self.brackets_label.pack(fill= "both", expand= True)

        self.button_frame = Frame(self)
        self.button_frame.place(relheight=0.18, relwidth=0.33, rely=0.82, relx=0.67)

        self.brackets_button = Button(self.button_frame, text= f"Br_calc[{self.name}]")
        self.brackets_button.pack(fill= "both", expand= True)

        self.calc_button = Button(self.button_frame, text= f"Calc[{self.name}]")
        self.calc_button.pack(fill= "both", expand= True)

    def rename(self, name : str):
        self.name = name
        self.brackets_button.configure(text= f"Br_calc[{self.name}]")
        self.calc_button.configure(text= f"Calc[{self.name}]")