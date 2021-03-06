      
# Used to define what type of RPC is sent. 
class HandleTypes:
    ExceptionOccurred = 0
    RequestFileRead = 1
    RequestFileWrite = 2
    ReleaseFileWrite = 3
    RequestFileUpdate = 4
    RequestDirectoryContents = 5

# Used to define what type of error occurred. 
class ExceptionTypes:
    FileNotFound = 0
    FileIsLocked = 1
    DirectoryNotFound = 2
    UnspecifiedError = 3


def CreateOfSubType(serialized):
    subMessage = RpcMessage(serialized = serialized)

    if subMessage.Type == HandleTypes.ExceptionOccurred: 
        return ExceptionMessage(serialized=serialized)
    elif subMessage.Type == HandleTypes.RequestFileRead:
        return FileReadMessage(serialized=serialized)
    elif subMessage.Type == HandleTypes.RequestFileWrite:
        return FileWriteMessage(serialized=serialized)
    elif subMessage.Type == HandleTypes.ReleaseFileWrite:
        return FileReleaseMessage(serialized=serialized)
    elif subMessage.Type == HandleTypes.RequestFileUpdate:
        return FileUpdateMessage(serialized=serialized)
    elif subMessage.Type == HandleTypes.RequestDirectoryContents:
        return DirectoryMessage(serialized=serialized)


# Base Class for all RpcMessages.
class RpcMessage: 
    Type = None
    Args = None # Unformatted Args!

    #TODO: add function to automatically create the right subtype message.
    def __init__(self, t=None, args=None, serialized = None):
        if (serialized != None):
            self.Deserialize(serialized)
        else:
            self.Type = t
            self.Args = args
    
    
    def Deserialize(self, serialized):
        #TODO: This code looks evil. I don't like that. Improve this.
        msg = str(serialized[1:len(serialized) - 1])
        self.Type = int(msg[0])
        self.Args = msg[3 : len(msg)]
        
    def Serialize(self):
        return str([self.Type, self.Args])


# Specialized RpcMessage for Exceptions
class ExceptionMessage(RpcMessage):
    ExceptionType = 0 # see: ExceptionTypes
    ExceptionArgs = "" # Serialized RPC call that failed


    def __init__(self, exceptionType = None, exceptionArgs = None, serialized = None):
        self.ExceptionType = exceptionType
        self.ExceptionArgs = exceptionArgs

        RpcMessage.__init__(self, 
            HandleTypes.ExceptionOccurred, 
            [exceptionType, exceptionArgs], 
            serialized)

    def Serialize(self):
        return str([self.Type, self.ExceptionType, self.ExceptionArgs])

    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        serialized = self.Args

        self.ExceptionType = serialized[1]
        self.ExceptionArgs = serialized[4 : len(serialized) - 2]

        return self


class FileReadMessage(RpcMessage):
    File = ""


    def __init__(self, file = None, serialized = None):
        self.File = file

        RpcMessage.__init__(self, 
            HandleTypes.RequestFileRead,
            file,
            serialized)

    def Serialize(self):
        return str([self.Type, self.File])

    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        self.File = self.Args[1 : len(self.Args) - 1]

        return self


class FileWriteMessage(RpcMessage):
    File = ""


    def __init__(self, file = None, serialized = None):
        self.File = file

        RpcMessage.__init__(self, 
            HandleTypes.RequestFileWrite,
            file,
            serialized)

    def Serialize(self):
        return str([self.Type, self.File])

    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        self.File = self.Args[1 : len(self.Args) - 1]

        return self


class FileReleaseMessage(RpcMessage):
    File = ""


    def __init__(self, file = None, serialized = None):
        self.File = file

        RpcMessage.__init__(self, 
            HandleTypes.ReleaseFileWrite,
            file,
            serialized)

    def Serialize(self):
        return str([self.Type, self.File])

    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        self.File = self.Args[1 : len(self.Args) - 1]

        return self


class FileUpdateMessage(RpcMessage):
    File = ""


    def __init__(self, file = None, serialized = None):
        self.File = file

        RpcMessage.__init__(self, 
            HandleTypes.RequestFileUpdate,
            file,
            serialized)

    def Serialize(self):
        return str([self.Type, self.File])

    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        self.File = self.Args[1 : len(self.Args) - 1]

        return self


class DirectoryMessage(RpcMessage):
    BaseDirectory = ""
    Directories = []
    Files = []


    def __init__(self, baseDirectory = None, directories = [], files = [], serialized = None):
        self.BaseDirectory = baseDirectory
        self.Directories = directories
        self.Files = files
        
        RpcMessage.__init__(
            self, 
            t = HandleTypes.RequestDirectoryContents, 
            serialized = serialized)

    def Serialize(self):
        return str([self.Type, self.BaseDirectory, self.Directories, self.Files])
    
    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        serialized = self.Args

        args = serialized.split(", [")
        
        #grabs the root dir. 
        baseDir = args[0][1 : len(args[0]) - 1]
        dirEntries = []
        fileEntries = []
        
        # grabs the listed directories. 
        dirs = args[1].replace(", ", "'").split("'")
        dirCount = len(dirs)
        for i in range(dirCount): 
            if dirs[i] == "":
                continue

            d = None
            if i == dirCount - 1: 
                break
            elif i == 0:
                d = dirs[i][1 : len(dirs[i])]
            else: 
                d = dirs[i]
            dirEntries.append(d)

        # grabs the listed files. 
        files = args[2].replace(", ", "'").split("'")
        fileCount = len(files)
        for i in range(fileCount):
            if files[i] == "":
                continue

            f = None
            if i == fileCount - 1: 
                break
            elif i == 0:
                f = files[i][1 : len(files[i])]
            else: 
                f = files[i]
            fileEntries.append(f)


        self.BaseDirectory = baseDir
        self.Directories = dirEntries
        self.Files = fileEntries
        
        return self
