from HandleTypes import HandleTypes
from NfsClient import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar


class ClientView(NfsClient):
    # contains truple: tab, server, and current directory
    tabs = []

    def __init__(self):
        NfsClient.__init__(self)
        self.view = tk.Tk()
        self.view.title = "NFS Client View"
        self.BuildTabs()
        print("Client View Initialized")
        self.view.mainloop()

    def OnDirectoryClick(self, mouseEvent):
        listbox = mouseEvent.widget
        selectionIndex = mouseEvent.widget.curselection()
        selection = listbox.get(selectionIndex)
        
        truple = None
        for t in self.tabs:
            for o in t[0].winfo_children():
                if o == listbox:
                    truple = t
                    break
            if not truple == None:
                break
        
        if not truple[2][len(truple[2])-1] == "/":
            truple[2] += "/"
        truple[2] += selection[6 : len(selection)]

        if selection[1] == "d":
            self.RequestFillView(truple)
        else: 
            print("a file is selected")

    def BuildTabs(self):
        tabControl = ttk.Notebook(self.view)
        for connection in self.connections:
            self.BuildTab(connection, tabControl)
        tabControl.pack(expand=1, fill="both")

    def BuildTab(self, connection, tabControl):
            tab = ttk.Frame(tabControl)
            tabControl.add(tab, text=connection.GetAddress())
            
            scrollbar = ttk.Scrollbar(tab)
            scrollbar.pack(side=RIGHT, fill=Y)

            listbox = Listbox(tab, yscrollcommand=scrollbar.set, selectmode=SINGLE)
            listbox.bind("<Double-Button-1>", self.OnDirectoryClick)
            listbox.pack(side=LEFT, fill=BOTH)

            truple = [tab, connection, "/"]
            self.tabs.append(truple)
            self.RequestFillView(truple)

    def RequestFillView(self, truple):
        message = RpcMessage(HandleTypes.RequestDirectoryContents, truple[2])
        truple[1].SendMessage(message)

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
        args = args.split("', [")[1]
        args = args[1:len(args)-2].split("', '")
        
        tab = truple[0]
        
        listbox = tab.winfo_children()
        for o in listbox:
            if o.widgetName == "listbox":
                listbox = o
                break
        
        listbox.delete(0, END)

        for i in range(len(args)):
            current = args[i]
            
            if current == "":
                continue

            #TODO: All this string comparison stuff sucks.. Integrate Json or something, and use more objects.
            prefix = None
            if current[0] == "f":
                prefix = "(fil) "
            elif current[0] == "d":
                prefix = "(dir) "
            elif current[0] == "o":
                prefix = "(oth) "

            listbox.insert(i, prefix + current[1:len(current)])
            