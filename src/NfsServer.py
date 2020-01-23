import Configuration
from FileHandler import *
import os
from RpcServerThread import * 
from socket import *
import threading
from tkinter.filedialog import askdirectory


class NfsServer (threading.Thread): 
    connectionSemaphore = threading.BoundedSemaphore(value=1)
    currentConnections = 0
    maximumConnections = 5
    isActive = True
    
    def __init__(self):
        threading.Thread.__init__(self)
        print("Initializing Server On port: %s" % Configuration.Port)
        self.fileHandler = FileHandler(self, Configuration.GetRootDirectory())
        self.connectionPort = Configuration.Port

    def run(self):
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
            self.connectionSemaphore.acquire(self)
            self.currentConnections += 1
            self.connectionSemaphore.release()
            rpcThread.start()

        rpcSocket.close()

    def CloseConnection(self, rpcThread):
        self.connectionSemaphore.acquire(rpcThread)
        self.currentConnections -= 1
        self.connectionSemaphore.release()
    