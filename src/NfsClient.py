import Configuration
from ClientConnection import *
from HandleTypes import HandleTypes
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
            connection.start()
            self.connections.append(connection)
    
    #TODO: Remove this at some point. Can be added in UI.
    def PromptServerAddress(self):
        print("Fill in server address:")
        s = input()
        print("Fill in server root:")
        r = input()
        Configuration.AppendServerList([s, r])


    def OnMessageReceived(self, requestType, args):
        if requestType == HandleTypes.ExceptionOccurred:
            print("error")
        elif requestType == HandleTypes.RequestFileRead:
            self.OnFileReadGranted(args)
        elif requestType == HandleTypes.RequestFileWrite:
            self.OnFileWriteGranted(args)
        elif requestType == HandleTypes.ReleaseFileWrite:
            self.OnFileRelease(args)
        elif requestType == HandleTypes.RequestFileUpdate:
            self.OnFileUpdateGranted(args)
        elif requestType == HandleTypes.RequestDirectoryContents:
            self.OnDirectoryContentsReceived(args)

    def OnFileReadGranted(self, args):
        return
    def OnFileWriteGranted(self, args):
        return
    def OnFileRelease(self, args):
        return
    def OnFileUpdateGranted(self, args):
        return
    def OnDirectoryContentsReceived(self, args):
        return
