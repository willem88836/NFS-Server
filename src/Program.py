
# from NfsClient import *
# from NfsServer import *
# from ClientView import *

# localServer = NfsServer()
# localServer.name = "ServerThread"
# localServer.start()

# clientView = ClientView()




from RpcMessage import *

regMsg = RpcMessage(HandleTypes.ExceptionOccurred, "these are arguments")
print(regMsg.Serialize())



dirMsg = DirectoryMessage("/rootDirectory", 
    ["Folder 1","Folder 2","Folder 3","Folder 4"],
    ["File 1", "File 2", "File 3", "File 4"])
serDirMsg = dirMsg.Serialize()

dirMsg2 = DirectoryMessage(None, None, None)
dirMsg2.Deserialize(serDirMsg)
