from RpcMessage import *


class FileHandler:
    Root = ""

    def __init__(self, root):
        #TODO: test root existence. 
        self.root = root
        print("File handler initialized.")


    def Handle(self, requestType, args):
        #TODO: error if invalid root.

        if requestType == HandleTypes.ExceptionOccurred:
            print("error")    
        elif requestType == HandleTypes.RequestFileAccess:
            print ("file request")
            self.HandleRequestFileAccess(args)
        elif requestType == HandleTypes.ReleaseFileAccess:
            print ("release file")
        elif requestType == HandleTypes.RequestFileUpdate:
            print ("request file update")


    def HandleRequestFileAccess(self, args):
        completePath = self.Root + args



class HandleTypes:
    ExceptionOccurred = 0
    RequestFileAccess = 1
    ReleaseFileAccess = 2
    RequestFileUpdate = 3