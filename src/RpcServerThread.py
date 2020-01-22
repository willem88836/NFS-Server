import socket
from socket import *
import threading
import NfsBase
from RpcMessage import *


class RpcServerThread(threading.Thread): 

    def __init__(self, clientSocket, clientAddress, nfsServer, rpcHandler):
        threading.Thread.__init__(self)
        self.name = "RpcThread%s" % str(clientAddress)
        self.ClientSocket = clientSocket
        self.ClientAddress = clientAddress
        self.NfsServer = nfsServer
        self.Buffer = NfsBase.Buffer
        self.RpcHandler = rpcHandler
        print("Initialized: %s" % self.name)

    def run(self):
        try:
            isConnected = True

            print("%s is awaiting messages..." % self.name)

            while isConnected:
                message = self.ClientSocket.recv(NfsBase.Buffer).decode()
                print("%s received message: %s" % (self.name, str(message)))

                if message == "":
                    isConnected = False
                    continue
                
                rpcMessage = RpcMessage(message)
                self.RpcHandler.Handle(rpcMessage.Type, rpcMessage.Args)

        except Exception: 
            print("An error occured. thread %s terminated" % self.name)

        print("Thread %s closing..." % self.name)
        self.ClientSocket.close()
        self.NfsServer.CloseConnection(self)
