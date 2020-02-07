from socket import os
import threading
import Configuration
from RpcMessage import CreateOfSubType


class RpcServerThread(threading.Thread): 

    def __init__(self, clientSocket, clientAddress, nfsServer, rpcHandler):
        threading.Thread.__init__(self)
        self.name = "ServerRpcThread%s" % str(clientAddress)
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
        









    ## Pseudo-code. 

    STREAM_BUFFER = 65535 # cannot be more than 65535 (that's the general PC buffersize).. 
    cur_buffer_use = 0 # This number will probably exceed the max..
    MAXIMUM_SEGMENT_SIZE = 1480 # Double check this size. calculate the headers.


    def TransmitFile(self, path):
        #mostly pseudo-code.

        file = open(path, mode="r")
        fileSize = os.path.getsize(path) 

        fileChunkIndex = 0
        fileChunksTotal = fileSize / self.MAXIMUM_SEGMENT_SIZE # The total number of chunks inside the file.
        lastChunkSize = fileSize % self.MAXIMUM_SEGMENT_SIZE

        fileSize = 0 # fill this in. s
        streamedFileSize = 0 

        
        while streamedFileSize < fileSize:
            # Should be streaming.

            while self.cur_buffer_use >= self.STREAM_BUFFER:
                ## wait for a while, or till the buffer is empty enough.
                continue
            
            file.seek(fileChunkIndex * self.MAXIMUM_SEGMENT_SIZE)
            readLength = -1
            if fileChunkIndex == fileChunksTotal:
                readLength = lastChunkSize
            else:
                readLength = self.MAXIMUM_SEGMENT_SIZE

            fileChunkIndex += 1
            self.cur_buffer_use += readLength
            
            dataChunk = file.read(readLength)
            # send dataChunk.

        file.close()
