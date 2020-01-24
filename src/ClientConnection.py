import threading
import socket
import Configuration 
from socket import *
from RpcMessage import *


class ClientConnection (threading.Thread):
    def __init__(self, address, root):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((address, Configuration.Port))
        print("Client Connection Initialized to server (%s), with root (%s), and is ready to communicate..." % (address, root))

    def SendMessage(message):
        self.socket.send(message)

    def run(self):
        self.isRunning = True

        while self.isRunning:
            message = self.socket.recv(Configuration.Buffer).decode()
            print("%s received message: %s" % (self.name, str(message)))
            message = RpcMessage(None, None, message)
            