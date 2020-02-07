import Configuration
from ClientConnection import ClientConnection
from RpcMessage import ExceptionMessage, ExceptionTypes, HandleTypes
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


    def SendError(self, server):
        message = ExceptionMessage(ExceptionTypes.UnspecifiedError, "")
        for c in self.connections:
            if c.GetAddress() == server:
                c.SendMessage(message)
                break


    def OnMessageReceived(self, server, message):
        if message.Type == HandleTypes.ExceptionOccurred:
            print("error")
        elif message.Type  == HandleTypes.RequestFileRead:
            self.OnFileReadGranted(server, message)
        elif message.Type  == HandleTypes.RequestFileWrite:
            self.OnFileWriteGranted(server, message)
        elif message.Type  == HandleTypes.ReleaseFileWrite:
            self.OnFileRelease(server, message)
        elif message.Type  == HandleTypes.RequestFileUpdate:
            self.OnFileUpdateGranted(server, message)
        elif message.Type  == HandleTypes.RequestDirectoryContents:
            self.OnDirectoryContentsReceived(server, message)

    def OnFileReadGranted(self, server, message):
        return
    def OnFileWriteGranted(self, server, message):
        return
    def OnFileRelease(self, server, message):
        return
    def OnFileUpdateGranted(self, server, message):
        return
    def OnDirectoryContentsReceived(self, server, message):
        return
