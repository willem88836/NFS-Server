import socket
from socket import *
import threading
import NfsBase
from RpcMessage import *


class RpcServerThread(threading.Thread): 

    def __init__(self, clientSocket, clientAddress, nfsServer):
        threading.Thread.__init__(self)
        self.name = "RpcThread%s" % str(clientAddress)
        self.ClientSocket = clientSocket
        self.ClientAddress = clientAddress
        self.NfsServer = nfsServer
        self.Buffer = NfsBase.Buffer
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
                # forward to Rpc handler


        except Exception: 
            print("An error occured. thread %s terminated" % self.name)

        print("Thread %s closing..." % self.name)
        self.ClientSocket.close()
        self.NfsServer.CloseConnection(self)
