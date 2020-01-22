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
        p = self.root + '/' + args
        print("file read requested: %s" % p)

        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        else:
            msg = RpcMessage(HandleTypes.RequestFileRead, args)
        
        issuer.SendMessage(msg)

    def HandleRequestFileWrite(self, issuer, args):
        p = self.root + '/' + args
        print ("file write requested: %s" % p)

        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        elif self.IsLocked(p) and not self.LockOwnedBy(p, issuer):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileIsLocked, args])
        elif self.LockOwnedBy(p, issuer):
            msg = RpcMessage(HandleTypes.RequestFileWrite, args)
        else:
            self.CreateLock(p, issuer)
            msg = RpcMessage(HandleTypes.RequestFileWrite, args)

        issuer.SendMessage(msg)

    def HandleReleaseFileWrite(self, issuer, args):
        p = self.root + '/' + args
        print ("File release: %s" % p)

        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        elif self.IsLocked(p):
            if self.LockOwnedBy(p, issuer):
                self.ReleaseLock(p, issuer)
                msg = RpcMessage(HandleTypes.ReleaseFileWrite, args)
            else:
                msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileIsLocked, args])
        else:
            msg = RpcMessage(HandleTypes.ReleaseFileWrite, args)
            
        issuer.SendMessage(msg)


    def ReleaseAllLocks(self, issuer):
        self.lockSemaphore.acquire(issuer)
        for l in self.userLockTable[issuer]:
            del(self.fileLockTable[l])
        del(self.userLockTable[issuer])
        self.lockSemaphore.release()

    def IsLocked(self, p):
        return p in self.fileLockTable

    def CreateLock(self, p, issuer):
        self.lockSemaphore.acquire(issuer)
        self.fileLockTable[p] = issuer
        if not issuer in self.userLockTable:
            self.userLockTable[issuer] = []
        self.userLockTable[issuer].append(p)
        self.lockSemaphore.release()
        print("created lock for file: %s" % p)

    def ReleaseLock(self, p, issuer):
        self.lockSemaphore.acquire(issuer)
        self.userLockTable[issuer].remove(p)
        del(self.fileLockTable[p])
        if len(self.userLockTable[issuer]) == 0:
            del(self.userLockTable[issuer])
        self.lockSemaphore.release()
        print("Releasing lock for file: %s" %p)

    def LockOwnedBy(self, p, issuer):
        return issuer in self.userLockTable and p in self.userLockTable[issuer]
        
        
class HandleTypes:
    ExceptionOccurred = 0
    RequestFileRead = 1
    RequestFileWrite = 2
    ReleaseFileWrite = 3
    RequestFileUpdate = 4

class ExceptionTypes:
    FileNotFound = 0
    FileIsLocked = 1
