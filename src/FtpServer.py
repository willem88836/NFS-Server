from socket import *
import threading
import FtpBase
from RpcServerThread import * 

connectionSemaphore = threading.BoundedSemaphore(value=1)


class FtpServer: 

    currentConnections = 0
    maximumConnections = 5
    isActive = True
    
    def __init__(self):
        print("Initializing Server On port: %s" % FtpBase.Port)
        self.connectionPort = FtpBase.Port
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
    