from FileHandler import *
import NfsBase
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
        print("Initializing Server On port: %s" % NfsBase.Port)
        self.SetNfsRoot()
        self.connectionPort = NfsBase.Port
        self.StartReceivingConnections()


    def SetNfsRoot(self):
        r = ""

        if not os.path.isfile(NfsBase.RootLocation):
            print("root directory not set")
            if not os.path.isdir(NfsBase.ConfigPath):
                os.makedirs(NfsBase.ConfigPath)

            f = open(NfsBase.RootLocation, "w")
            r = askdirectory()
            f.writelines(r)
            f.close()
        else:
            print("root directory set")
            f = open(NfsBase.RootLocation, "r")
            r = f.read()
            f.close()

            if not os.path.isdir(r):
                print("could not find set root")
                r = askdirectory()
                f = open(NfsBase.RootLocation, "w")
                f.write(r)

            f.close()
        
        self.fileHandler = FileHandler(r)


    def StartReceivingConnections(self):
        rpcSocket = socket(AF_INET, SOCK_STREAM)
        rpcSocket.bind(('', self.connectionPort))
        rpcSocket.listen(1)

        while self.isActive: 
            while self.currentConnections >= self.maximumConnections:
                continue

            print("Awaiting Connection...")
            clientSocket, clientIP = rpcSocket.accept()
            
            rpcThread = RpcServerThread(clientSocket, clientIP, self)
            connectionSemaphore.acquire(self)
            self.currentConnections += 1
            connectionSemaphore.release()
            rpcThread.start()

        rpcSocket.close()

    def CloseConnection(self, rpcThread):
        connectionSemaphore.acquire(rpcThread)
        self.currentConnections -= 1
        connectionSemaphore.release()
    