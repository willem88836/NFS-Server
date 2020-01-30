import socket
from socket import *
import threading
import Configuration
from RpcMessage import *


class RpcServerThread(threading.Thread): 

    def __init__(self, clientSocket, clientAddress, nfsServer, rpcHandler):
        threading.Thread.__init__(self)
        self.name = "RpcThread%s" % str(clientAddress)
        self.ClientSocket = clientSocket
        self.ClientAddress = clientAddress
        self.NfsServer = nfsServer
        self.Buffer = Configuration.Buffer
        self.RpcHandler = rpcHandler
        print("Initialized: %s" % self.name)

    def run(self):
        try:
            isConnected = True
            
            print("%s is awaiting messages..." % self.name)

            while isConnected:
                message = self.ClientSocket.recv(Configuration.Buffer).decode()
                print("%s received message: %s" % (self.name, str(message)))

                if message == "":
                    isConnected = False
                    continue
                
                rpcMessage = CreateOfSubType(message)
                self.RpcHandler.Handle(self, rpcMessage)
        except Exception as e: 
            print("An error occured: (%s). thread %s terminated" % (format(e), self.name))
        finally:
            print("Thread %s closing..." % self.name)
            self.RpcHandler.ReleaseAllLocks(self)
            self.ClientSocket.close()
            self.NfsServer.CloseConnection(self)

    def SendMessage(self, message):
        msg = str(message.Serialize()).encode()
        self.ClientSocket.send(msg)
        print("sent message (%s) from %s" % (msg, self.name))

    def Terminate(self):
        self.isConnected = False
        