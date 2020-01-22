import Configuration
from FileHandler import *
import os
from RpcServerThread import * 
from socket import *
import threading
from tkinter.filedialog import askdirectory

connectionSemaphore = threading.BoundedSemaphore(value=1)


class NfsServer: 

    currentConnections = 0
    maximumConnections = 5
    isActive = True
    
    def __init__(self):
        print("Initializing Server On port: %s" % Configuration.Port)
        self.fileHandler = FileHandler(Configuration.GetRootDirectory())
        self.connectionPort = Configuration.Port
        self.StartReceivingConnections()


    def StartReceivingConnections(self):
        rpcSocket = socket(AF_INET, SOCK_STREAM)
        rpcSocket.bind(('', self.connectionPort))
        rpcSocket.listen(1)

        while self.isActive: 
            while self.currentConnections >= self.maximumConnections:
                continue

            print("Awaiting Connection...")
            clientSocket, clientIP = rpcSocket.accept()
            
            rpcThread = RpcServerThread(clientSocket, clientIP, self, self.fileHandler)
            connectionSemaphore.acquire(self)
            self.currentConnections += 1
            connectionSemaphore.release()
            rpcThread.start()

        rpcSocket.close()

    def CloseConnection(self, rpcThread):
        connectionSemaphore.acquire(rpcThread)
        self.currentConnections -= 1
        connectionSemaphore.release()
    