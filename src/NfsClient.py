import Configuration
from RpcMessage import *
import socket
from socket import *
import threading
import json

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
            for e in serverList:
                # TODO: Figure out what to do with the root directory
                r = json.JSONDecoder.decode(e) 
                connection = ClientConnection(e[0], e[1])
                self.connections.append(connection) #TODO: continue here. 

    def PromptServerAddress(self):
        print("Fill in server address:")
        s = input()
        print("Fill in server root:")
        r = input()
        Configuration.AppendServerList([s, r])



class ClientConnection (threading.Thread):
    def __init__(self, s, r):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connection((s, Configuration.Port))

        print("client ready to communicate")

    def SendMessage(message):
        self.socket.send(message)

    def run(self):
        self.isRunning = True

        while self.isRunning:
            message = self.socket.recv(Configuration.Buffer).decode()
            print("%s received message: %s" % (self.name, str(message)))

            message = RpcMessage(None, None, message)
            