import os
from RpcMessage import *
from RpcServerThread import *
import threading

class FileHandler:
    lockSemaphore = threading.BoundedSemaphore(value=1)
    fileLockTable = {}
    userLockTable = {}

    def __init__(self, nfsServer, root):
        self.nfsServer = nfsServer
        self.root = root
        print("File handler initialized.")


    def Handle(self, issuer, requestType, args):
        if requestType == HandleTypes.ExceptionOccurred:
            print("error")
        elif requestType == HandleTypes.RequestFileRead:
            self.HandleRequestFileRead(issuer, args)
        elif requestType == HandleTypes.RequestFileWrite:
            self.HandleRequestFileWrite(issuer, args)
        elif requestType == HandleTypes.ReleaseFileWrite:
            self.HandleReleaseFileWrite(issuer, args)
        elif requestType == HandleTypes.RequestFileUpdate:
            print ("request file update")


    def HandleRequestFileRead(self, issuer, args):
        p = self.root + '\\' + args
        print("file read requested: %s" % p)

        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        else:
            msg = RpcMessage(HandleTypes.RequestFileRead, args)
        
        issuer.SendMessage(msg)

    def HandleRequestFileWrite(self, issuer, args):
        p = self.root + '\\' + args
        print ("file write requested: %s" % p)

        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        elif IsLocked(p) and not LockOwnedBy(p, issuer):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileIsLocked, args])
        elif LockOwnedBy(p, issuer):
            msg = RpcMessage(HandleTypes.RequestFileWrite, args)
        else:
            CreateLock(p, issuer)
            msg = RpcMessage(HandleTypes.RequestFileWrite, args)

        issuer.SendMessage(msg)

    def HandleReleaseFileWrite(self, issuer, args):
        p = self.root + '\\' + args
        print ("File release: %s" % p)

        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        elif IsLocked(p):
            if LockOwnedBy(p, issuer):
                ReleaseLock(p, issuer)
                msg = RpcMessage(HandleTypes.ReleaseFileWrite, args)
            else:
                msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileIsLocked, args])
        else:
            msg = RpcMessage(HandleTypes.ReleaseFileWrite, args)
            
        issuer.SendMessage(msg)


    def ReleaseAllLocks(issuer):
        lockSemaphore.acquire(issuer)
        for l in userLockTable[issuer]:
            fileLockTable.remove(l)
        userLockTable.remove(issuer)
        lockSemaphore.release()

    def IsLocked(p):
        return p in fileLockTable

    def CreateLock(p, issuer):
        lockSemaphore.acquire(issuer)
        fileLockTable[p] = issuer
        userLockTable[issuer].append(p)
        lockSemaphore.release()
        print("created lock for file: %s" % p)

    def ReleaseLock(p, issuer):
        lockSemaphore.acquire(issuer)
        userLockTable[issuer].remove(p)
        fileLockTable.remove(p)
        lockSemaphore.release()
        print("Releasing lock for file: %s" %p)

    def LockOwnedBy(p, issuer):
        return p in userLockTable[issuer]
        
        
class HandleTypes:
    ExceptionOccurred = 0
    RequestFileRead = 1
    RequestFileWrite = 2
    ReleaseFileWrite = 3
    RequestFileUpdate = 4

class ExceptionTypes:
    FileNotFound = 0
    FileIsLocked = 1
