from tkinter import Toplevel
from tkinter import Frame, X
from tkinter import Listbox
from tkinter import LEFT, BOTH, Scrollbar, RIGHT, END

class Relations(Toplevel):

    def __init__(self, relations):
        Toplevel.__init__(self)
        self.geometry("700x470")
        self.title("Relations")
        self.relations = relations

        self.top = Frame(self, height=700, bg='white')
        self.top.pack(fill=X)
        self.listbox = Listbox(self.top, width=80)
        self.listbox.pack(side = LEFT, fill = BOTH)
        self.scrollbar = Scrollbar(self.top)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        for values in relations:
            self.listbox.insert(END, values)
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)