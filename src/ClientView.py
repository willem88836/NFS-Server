from NfsClient import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import Scrollbar


class ClientView(NfsClient):
    tabs = [] # Contains ExplorerTabs

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
        
        tab = None
        for t in self.tabs:
            for o in t.Tab.winfo_children():
                if o == listbox:
                    tab = t
                    break
            if not tab == None:
                break
        

        if (tab.IsDirectory(selection)):
            tab.AppendDirectory(selection)
            self.RequestFillView(tab)
        else:
            #TODO: add a prompt for readwrite or readonly
            filePath =  tab.CombineDirectoryWith(selection)
            readFileMessage = FileReadMessage(file = filePath)
            tab.Connection.SendMessage(readFileMessage)

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

            listbox = Listbox(tab, yscrollcommand=scrollbar.set, selectmode=SINGLE, width=150, height=20)
            listbox.bind("<Double-Button-1>", self.OnDirectoryClick)
            listbox.pack(side=LEFT, fill=BOTH, padx=15, pady=15)

            explorerTab = ExplorerTab(tab, connection, "/")
            self.tabs.append(explorerTab)
            self.RequestFillView(explorerTab)

    def RequestFillView(self, explorerTab):
        message = DirectoryMessage(explorerTab.CurrentDirectory) 
        explorerTab.Connection.SendMessage(message)

    def OnDirectoryContentsReceived(self, server, message):
        explorerTab = None
        for tab in self.tabs:
            if tab.Connection.GetAddress() == server:
                explorerTab = tab

        if explorerTab == None:
            print("server has no table")
            self.SendError(server) # TODO: remove this.
            return
        
        explorerTab.UpdateContents(
            message.BaseDirectory,
            message.Directories, 
            message.Files)
            

# contains truple: tab, server, and current directory
class ExplorerTab:
    Tab = None
    Connection = None
    CurrentDirectory = None
    
    Directories = []
    Files = []


    def __init__(self, tab, connection, directory):
        self.Tab = tab
        self.Connection = connection
        self.CurrentDirectory = directory
        
    def AppendDirectory(self, path):
        self.CurrentDirectory = self.CombineDirectoryWith(path)

    def CombineDirectoryWith(self, path):
        pseudo = self.CurrentDirectory
        if not pseudo[len(pseudo) - 1] == "/":
            pseudo += "/"
        pseudo += path
        return pseudo

    def UpdateContents(self, directory, directories, files):
        self.CurrentDirectory = directory
        self.Files = files
        self.Directories = directories 

        # Updates the listbox contents
        listbox = None
        for o in self.Tab.winfo_children():
            if o.widgetName == "listbox":
                listbox = o
        
        listbox.delete(0, END)

        i = 0
        for d in self.Directories:
            listbox.insert(i, d)
            i += 1
        
        for f in self.Files:
            listbox.insert(i, f)
            i += 1


    def IsDirectory(self, name):
        for a in self.Directories:
            if a == name:
                return True
        return False

    def IsFile(self, name):
        for f in self.Files:
            if f == name:
                return True
        return False
