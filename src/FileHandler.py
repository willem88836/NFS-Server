from RpcMessage import *
import os

class FileHandler:
    def __init__(self, nfsServer, root):
        self.nfsServer = nfsServer
        self.root = root
        print("File handler initialized.")


    def Handle(self, requestType, args):
        #TODO: error if invalid root.

        if requestType == HandleTypes.ExceptionOccurred:
            print("error")    
        elif requestType == HandleTypes.RequestFileAccess:
            print ("file read request")
            self.HandleRequestFileRead(args)
        elif requestType == HandleTypes.ReleaseFileAccess:
            print ("release file")
        elif requestType == HandleTypes.RequestFileUpdate:
            print ("request file update")


    def HandleRequestFileRead(self, args):
        p = self.root + '\\' + args
        print("file requested: %s" % p)

        if not os.path.isfile(p)
            errorMessage = RpcMessage(HandleTypes.ExceptionOccurred, ExceptionTypes.FileNotFound)
            return
        
        message = RpcMessage(HandleTypes.RequestFileRead, path)
        #TODO: Start Stream



    def IsLocked(p):
        return False
        


class HandleTypes:
    ExceptionOccurred = 0
    RequestFileRead = 1
    RequestFileWrite = 2
    ReleaseFileWrite = 3
    RequestFileUpdate = 4

class ExceptionTypes:
    FileNotFound = 0
