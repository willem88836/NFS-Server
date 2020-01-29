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

        self.HandleDirectoryContents(None, "")


    def Handle(self, issuer, requestType, args):
        if requestType == HandleTypes.ExceptionOccurred:
            issuer.Terminate()
        elif requestType == HandleTypes.RequestFileRead:
            self.HandleRequestFileRead(issuer, args)
        elif requestType == HandleTypes.RequestFileWrite:
            self.HandleRequestFileWrite(issuer, args)
        elif requestType == HandleTypes.ReleaseFileWrite:
            self.HandleReleaseFileWrite(issuer, args)
        elif requestType == HandleTypes.RequestFileUpdate:
            self.HandleFileUpdate(issuer, args)
        elif requestType == HandleTypes.RequestDirectoryContents:
            self.HandleDirectoryContents(issuer, args)


    def HandleRequestFileRead(self, issuer, args):
        p = self.root + args
        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        else:
            msg = RpcMessage(HandleTypes.RequestFileRead, args)
        
        issuer.SendMessage(msg)
        print("file read requested: %s" % p)

    def HandleRequestFileWrite(self, issuer, args):
        p = self.root + args
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
        print ("file write requested: %s" % p)

    def HandleReleaseFileWrite(self, issuer, args):
        p = self.root + args
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
        print ("File release: %s" % p)

    def HandleFileUpdate(self, issuer, args):
        p = self.root + args
        msg = None

        if not os.path.isfile(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileNotFound, args])
        elif not self.LockOwnedBy(p, issuer):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.FileIsLocked, args])
        else: 
            msg = RpcMessage(HandleTypes.RequestFileUpdate, args)

        issuer.SendMessage(msg)
        print("File update requested: %s" % p)

    def HandleDirectoryContents(self, issuer, args):
        p = self.root + args
        msg = None
        
        if not os.path.isdir(p):
            msg = RpcMessage(HandleTypes.ExceptionOccurred, [ExceptionTypes.DirectoryNotFound, args])
        else:
            dirEntries = os.listdir(p)

            files = []
            directories = []

            for e in dirEntries:
                p = self.root + '/' + e
                if os.path.isdir(p):
                    directories.append(e)
                elif os.path.isfile(p):
                    files.append(e)
                else:
                    print("found object that is not supported: %s" % p)
            
            args = [args, directories, files]

            print (args)
            msg = RpcMessage(HandleTypes.RequestDirectoryContents, args)
        
        return
        issuer.SendMessage(msg)
        print("Directory contents requested: %s" % p)


    def ReleaseAllLocks(self, issuer):
        self.lockSemaphore.acquire(issuer)
        if issuer in self.userLockTable:
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
   