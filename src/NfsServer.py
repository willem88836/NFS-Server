import Configuration
from FileHandler import *
import os
from RpcServerThread import * 
from socket import *
import threading
from tkinter.filedialog import askdirectory

#TODO: Create Server View
class NfsServer (threading.Thread): 
    connectionSemaphore = threading.BoundedSemaphore(value=1)
    maximumConnections = 5
    activeConnections = []
    isActive = False
    
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
        self.isActive = True

        while self.isActive: 
            while len(self.activeConnections) >= self.maximumConnections:
                continue

            print("Awaiting Connection...")
            clientSocket, clientIP = rpcSocket.accept()
            
            rpcThread = RpcServerThread(clientSocket, clientIP, self, self.fileHandler)
            self.connectionSemaphore.acquire(self)
            self.activeConnections.append(rpcThread)
            self.connectionSemaphore.release()
            rpcThread.start()

        rpcSocket.close()

    def CloseConnection(self, rpcThread):
        self.connectionSemaphore.acquire(rpcThread)
        self.activeConnections.remove(rpcThread)
        self.connectionSemaphore.release()
    
    def IsActive(self):
        return self.isActive

    def Terminate(self):
        self.connectionSemaphore.acquire(self)
        for c in self.activeConnections:
            c.Terminate()
        self.activeConnections.clear()
        self.connectionSemaphore.release()
        