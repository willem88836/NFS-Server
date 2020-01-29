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


    def Handle(self, issuer, rpcMessage):
        if rpcMessage.Type == HandleTypes.ExceptionOccurred:
            issuer.Terminate()
        elif rpcMessage.Type == HandleTypes.RequestFileRead:
            fileReadMessage = FileReadMessage(None).Deserialize(rpcMessage.Args)
            self.HandleRequestFileRead(issuer, fileReadMessage)
        elif rpcMessage.Type == HandleTypes.RequestFileWrite:
            fileWriteMessage = FileWriteMessage(None).Deserialize(rpcMessage.Args)
            self.HandleRequestFileWrite(issuer, fileWriteMessage)
        elif rpcMessage.Type == HandleTypes.ReleaseFileWrite:
            fileReleaseMessage = FileReleaseMessage(None).Deserialize(rpcMessage.Args)
            self.HandleReleaseFileWrite(issuer, fileReleaseMessage)
        elif rpcMessage.Type == HandleTypes.RequestFileUpdate:
            fileUpdateMessage = FileUpdateMessage(None).Deserialize(rpcMessage.Args)
            self.HandleFileUpdate(issuer, fileUpdateMessage)
        elif rpcMessage.Type == HandleTypes.RequestDirectoryContents:
            directoryMessage = DirectoryMessage(None, None, None).Deserialize(rpcMessage.Args)
            self.HandleDirectoryContents(issuer, directoryMessage)


    def HandleRequestFileRead(self, issuer, message):
        p = self.root + message.File
        msg = None

        if not os.path.isfile(p):
            msg = ExceptionMessage(ExceptionTypes.FileNotFound, message.Serialize())
        else:
            msg = FileReadMessage(message.File)
        
        issuer.SendMessage(msg)
        print("file read requested: %s" % p)

    def HandleRequestFileWrite(self, issuer, message):
        p = self.root + message.File
        msg = None

        if not os.path.isfile(p):
            msg = ExceptionMessage(ExceptionTypes.FileNotFound, message.Serialize())
        elif self.IsLocked(p) and not self.LockOwnedBy(p, issuer):
            msg = ExceptionMessage(ExceptionTypes.FileIsLocked, message.Serialize())
        elif self.LockOwnedBy(p, issuer):
            msg = FileWriteMessage(message.File)
        else:
            self.CreateLock(p, issuer)
            msg = FileWriteMessage(message.File)

        issuer.SendMessage(msg)
        print ("file write requested: %s" % p)

    def HandleReleaseFileWrite(self, issuer, message):
        p = self.root + message.File
        msg = None

        if not os.path.isfile(p):
            msg = ExceptionMessage(ExceptionTypes.FileNotFound, message.Serialize())
        elif self.IsLocked(p):
            if self.LockOwnedBy(p, issuer):
                self.ReleaseLock(p, issuer)
                msg = FileReleaseMessage(message.File)
            else:
                msg = ExceptionMessage(ExceptionTypes.FileIsLocked, message.Serialize())
        else:
            msg = FileReleaseMessage(message.File)
            
        issuer.SendMessage(msg)
        print ("File release: %s" % p)

    def HandleFileUpdate(self, issuer, message):
        p = self.root + message.File
        msg = None

        if not os.path.isfile(p):
            msg = ExceptionMessage(ExceptionTypes.FileNotFound, message.Serialize())
        elif not self.LockOwnedBy(p, issuer):
            msg = ExceptionMessage(ExceptionTypes.FileIsLocked, message.Serialize())
        else: 
            msg = FileUpdateMessage(message.File)

        issuer.SendMessage(msg)
        print("File update requested: %s" % p)

    def HandleDirectoryContents(self, issuer, message):
        p = self.root + message.BaseDirectory
        msg = None
        
        if not os.path.isdir(p):
            msg = ExceptionMessage(ExceptionTypes.DirectoryNotFound, message.Serialize())
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
            
            msg = DirectoryMessage(message.BaseDirectory, directories, files)
        
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
   