from NfsClient import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar
from HandleTypes import HandleTypes


class ClientView(NfsClient):
    tabs = []

    def __init__(self):
        NfsClient.__init__(self)
        self.view = tk.Tk()
        self.view.title = "NFS Client View"
        self.BuildTabs()
        print("Client View Initialized")
        self.view.mainloop()

    def BuildTabs(self):
        tabControl = ttk.Notebook(self.view)
        for connection in self.connections:
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=connection.GetAddress())
            tabControl.pack(expand=1, fill="both")
            
            # tab, server, and current directory
            truple = [tab, connection, ""]
            self.tabs.append(truple)

            scrollbar = Scrollbar(tab)
            scrollbar.pack(side = RIGHT, fill = Y)
            self.myList = Listbox(tab, yscrollcommand=scrollbar.set)
            self.RequestFillView(truple)

    def RequestFillView(self, truple):
        message = RpcMessage(HandleTypes.RequestDirectoryContents, truple[2])
        truple[1].SendMessage(message)
