import socket
from socket import *
import threading
import FtpBase


class RpcServerThread(threading.Thread): 

    def __init__(self, clientSocket, clientAddress, ftpServer):
        threading.Thread.__init__(self)
        self.name = "RpcThread%s" % str(clientAddress)
        self.ClientSocket = clientSocket
        self.ClientAddress = clientAddress
        self.FtpServer = ftpServer
        self.Buffer = FtpBase.Buffer
        print("Initialized: %s" % self.name)

    def run(self):
        try:
            isConnected = True

            print("%s is awaiting messages..." % self.name)

            while isConnected:
                message = self.ClientSocket.recv(FtpBase.Buffer).decode()
                print("%s received message: %s" % (self.name, str(message)))

                if message == "":
                    isConnected = False
                    continue
                
                # Decode message;
                # Forward message to Request Handler
        except Exception: 
            print("An error occured. thread %s terminated" % self.name)

        print("Thread %s closing..." % self.name)
        self.ClientSocket.close()
        self.FtpServer.CloseConnection(self)
