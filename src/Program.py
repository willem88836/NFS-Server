
# from NfsClient import *
from NfsServer import *
from ClientView import *

localServer = NfsServer()
localServer.name = "ServerThread"
localServer.start()

clientView = ClientView()
