from tkinter import Tk
from view import View

class Controller():
    def __init__(self):
        self.root = Tk()
        self.view = View(self.root)
        self.model = None

    def run(self):
        self.root.mainloop()