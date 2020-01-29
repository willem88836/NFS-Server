      
class HandleTypes:
    ExceptionOccurred = 0
    RequestFileRead = 1
    RequestFileWrite = 2
    ReleaseFileWrite = 3
    RequestFileUpdate = 4
    RequestDirectoryContents = 5


class RpcMessage: 
    Type = None
    Args = None

    def __init__(self, t, args, serialized = None):
        if (serialized != None):
            self.Deserialize(serialized)
        else:
            self.Type = t
            self.Args = args

    def Deserialize(self, deserializable):
        #TODO: This code looks evil. I don't like that. Improve this.
        msg = str(deserializable[1:len(deserializable)-1])
        self.Type = int(msg[0])
        self.Args = msg[3 : len(msg)]
        
    def Serialize(self):
        wrap = [self.Type, self.Args]
        return wrap



class ExceptionMessage(RpcMessage):
    ExceptionType = 0
    ExceptionArgs = ""

    def __init__(self, exceptionType, args):
        RpcMessage.__init__(self, 
        HandleTypes.ExceptionOccurred, 
        [exceptionType, args])

    def Serialize(self):
        return str(self.Args)

    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        serialized = self.Args





class DirectoryMessage(RpcMessage):
    BaseDirectories = ""
    Directories = []
    Files = []

    def __init__(self, baseDirectories, directories, files):
        RpcMessage.__init__(self, 
            HandleTypes.RequestDirectoryContents, 
            [baseDirectories, directories, files], 
            None)

        self.BaseDirectories = baseDirectories
        self.Directories = directories
        self.Files = files

    def Serialize(self):
        return str([self.Type, self.BaseDirectories, self.Directories, self.Files])
    
    def Deserialize(self, serialized):
        RpcMessage.Deserialize(self, serialized)
        serialized = self.Args

        args = serialized.split(", ['")
        
        baseDir = args[0][1 : len(args[0]) - 1]
        dirEntries = []
        fileEntries = []
        
        dirs = args[1].split("', '")
        dirCount = len(dirs)
        for i in range(dirCount): 
            d = None
            if i == dirCount - 1: 
                d = dirs[i][0 : len(dirs[i]) - 2]
            else: 
                d = dirs[i]
            dirEntries.append(d)

        files = args[2].split("', '")
        fileCount = len(files)
        for i in range(fileCount):
            f = None
            if i == dirCount - 1: 
                f = files[i][0 : len(files[i]) - 2]
            else: 
                f = files[i]
            fileEntries.append(f)


        self.BaseDirectories = baseDir
        self.Directories = dirEntries
        self.Files = fileEntries
        
        self.Args = [self.BaseDirectories, self.Directories, self.Files]
