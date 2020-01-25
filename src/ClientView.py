from NfsClient import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar
from HandleTypes import HandleTypes


class ClientView(NfsClient):
    # contains truple: tab, server, and current directory
    tabs = []
    dirClickVar = None

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
            
            truple = [tab, connection, ""]
            self.tabs.append(truple)

            scrollbar = Scrollbar(tab)
            scrollbar.pack(side = RIGHT, fill = Y)
            self.myList = Listbox(tab, yscrollcommand=scrollbar.set)
            self.RequestFillView(truple)

    def RequestFillView(self, truple):
        message = RpcMessage(HandleTypes.RequestDirectoryContents, truple[2])
        truple[1].SendMessage(message)


    def OnDirectoryClicked(self):
        print(self.dirClickVar)

    def OnDirectoryContentsReceived(self, server, args):
        truple = None
        for t in self.tabs:
            if t[1].GetAddress() == server:
                truple = t

        if truple == None:
            print("server has no table")
            self.SendError(server)
            return

        #TODO: Magic!
        args = args[7:len(args)-3].split("', '")
        
        col = 0
        for d in args:
            dirButton = ttk.Button(truple[0], text=d, variable=self.dirClickVar, command=self.OnDirectoryClicked)
            # dirButton.grid(column=col, row = 0)
            col += 1
