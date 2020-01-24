import Configuration
from RpcMessage import *
import socket
from socket import *
import threading
from ClientConnection import *


class NfsClient:
    
    connections = []

    def __init__(self):
        self.ConnectToServer()

    def ConnectToServer(self):
        serverList = Configuration.GetServerList()

        if len(serverList) == 0:
            print("no servers set")
            self.PromptServerAddress()
            self.ConnectToServer()
        else: 
            for entry in serverList:
                if entry == "":
                    continue
                # TODO: this does not seem like a healthy way to split.
                entry = entry.split(sep=", ")
                address = str(entry[0][2:len(entry[0]) - 1])
                root = str(entry[1][1:len(entry[1]) - 3])
                connection = ClientConnection(address, root)
                connection.start()
                self.connections.append(connection)

    def PromptServerAddress(self):
        print("Fill in server address:")
        s = input()
        print("Fill in server root:")
        r = input()
        Configuration.AppendServerList([s, r])
