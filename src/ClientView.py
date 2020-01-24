from NfsClient import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar


class ClientView(NfsClient):
    def __init__(self):
        NfsClient.__init__(self)
        self.view = tk.Tk()
        self.view.title = "NFS Client View"
        #TODO: create tabs, per connection
        self.BuildView()
        # self.FillView(self)
        self.view.mainloop()

    def BuildTabs(self):
        print (" asdf")
        #TODO: create tabs per connection, per tab create view. 

    def BuildView(self):
        scrollbar = Scrollbar(self.view)
        scrollbar.pack(side = RIGHT, fill = Y)
        self.myList = Listbox(self.view, yscrollcommand=scrollbar.set)

    def FillView(self, directory):
        print("adf")
