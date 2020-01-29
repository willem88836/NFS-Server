import Configuration
from ClientConnection import *
from RpcMessage import *
import socket
from socket import *
import threading

class NfsClient:
    
    connections = []

    def __init__(self):
        self.ConnectToServer()

    def ConnectToServer(self):
        serverList = Configuration.GetServerList()

        print("Connecting with %i different servers" % len(serverList))

        for entry in serverList:
            if entry == "":
                continue
            # TODO: this does not seem like a healthy way to split.
            entry = entry.split(sep=", ")
            address = str(entry[0][2:len(entry[0]) - 1])
            root = str(entry[1][1:len(entry[1]) - 3])
            connection = ClientConnection(self, address, root)
            connection.name = "ClientConnection%s" % entry
            connection.start()
            self.connections.append(connection)
    
    #TODO: Remove this at some point. Can be added in UI.
    def PromptServerAddress(self):
        print("Fill in server address:")
        s = input()
        print("Fill in server root:")
        r = input()
        Configuration.AppendServerList([s, r])


    def SendError(self, server):
        message =  RpcMessage(t=HandleTypes.ExceptionOccurred, args="")
        for c in self.connections:
            if c.GetAddress() == server:
                c.SendMessage(message)
                break


    def OnMessageReceived(self, server, requestType, args):
        if requestType == HandleTypes.ExceptionOccurred:
            print("error")
        elif requestType == HandleTypes.RequestFileRead:
            self.OnFileReadGranted(server, args)
        elif requestType == HandleTypes.RequestFileWrite:
            self.OnFileWriteGranted(server, args)
        elif requestType == HandleTypes.ReleaseFileWrite:
            self.OnFileRelease(server, args)
        elif requestType == HandleTypes.RequestFileUpdate:
            self.OnFileUpdateGranted(server, args)
        elif requestType == HandleTypes.RequestDirectoryContents:
            self.OnDirectoryContentsReceived(server, args)

    def OnFileReadGranted(self, server, args):
        return
    def OnFileWriteGranted(self, server, args):
        return
    def OnFileRelease(self, server, args):
        return
    def OnFileUpdateGranted(self, server, args):
        return
    def OnDirectoryContentsReceived(self, server, args):
        return
