from tkinter import Frame, Menu, Tk, simpledialog
from tkinter.ttk import Notebook

from calculatortab import CalculatorTab

class View:
    def __init__(self, root : Tk):
        self.root = root
        self.size = (800, 600)
        self.background = "#ffe0ca"
        self.tab_count = 0

        self._setup_main_layout()

    def _setup_main_layout(self):
        self.root.title("Calculator")
        self.root.geometry(f"{self.size[0]}x{self.size[1]}")

        self.notebook = Notebook(self.root)
        self.notebook.pack(fill= "both", expand= True)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_chaged)
        self.notebook.bind("<Button-1>", self.on_tab_left_click)
        self.notebook.bind("<Button-3>", self.on_tab_right_click)
        self.notebook.bind("<Double-Button-1>", self.on_tab_double_click)

        self.add_tab_button = Frame(self.notebook, name= "add_tab")
        self.notebook.add(self.add_tab_button, text= "+")

        self.add_tab()

    def on_tab_chaged(self, event):
        if event.widget.select().split(".")[-1] == "add_tab":
            event.widget.select(len(event.widget.tabs()) - 2)
    
    def on_tab_left_click(self, event):
        tab_index = event.widget.index(f"@{event.x},{event.y}")
        if event.widget.tab(tab_index, "text") == "+":
            self.add_tab()

    def add_tab(self):
        tab = CalculatorTab(self.notebook, str(self.tab_count))
        tab.pack(side= "top", fill="both", expand= True)
        self.notebook.insert(len(self.notebook.tabs()) - 1, tab, text= str(self.tab_count))
        self.notebook.select(tab)
        self.tab_count += 1
    
    def delete_tab(self, tab_index : int):
        tab = self.root.nametowidget(self.notebook.tabs()[tab_index])
        self.notebook.forget(tab_index)
        tab.pack_forget()
        del tab
    
    def rename_tab(self, tab_index : int):
        current_name = self.notebook.tab(tab_index, "text")
        new_name = simpledialog.askstring("Перейменувати вкладку", "Введіть нову назву вкладки:", initialvalue=current_name)
        if new_name:
            self.notebook.tab(tab_index, text= new_name)
            self.root.nametowidget(self.notebook.tabs()[tab_index]).rename(new_name)

    def on_tab_right_click(self, event):
        tab_index = event.widget.index(f"@{event.x},{event.y}")
        if event.widget.tab(tab_index, "text") == "+":
            return
        context_menu = Menu(tearoff= 0)
        context_menu.add_command(label= "Перейменувати", command= lambda: self.rename_tab(tab_index))
        context_menu.add_command(label= "Видалити", command= lambda: self.delete_tab(tab_index))
        context_menu.post(event.x_root, event.y_root)

    def on_tab_double_click(self, event):
        tab_index = event.widget.index(f"@{event.x},{event.y}")
        if event.widget.tab(tab_index, "text") == "+":
            return
        self.delete_tab(tab_index)