import threading
import socket
import Configuration 
from socket import socket, AF_INET, SOCK_STREAM
from RpcMessage import CreateOfSubType


class ClientConnection (threading.Thread):
    isConnected = False
    isInitialized = False

    def __init__(self, parent, address, root):
        print("starting connection")
        threading.Thread.__init__(self)
        self.parent = parent
        self.address = address
        self.root = root
        self.socket = socket(AF_INET, SOCK_STREAM)

        self.name = "ClientRpcThread(%s, %s)" % (address, root)
        
        try:
            self.socket.connect((address, Configuration.Port))
            self.isConnected = True
            print("Client Connection Initialized to server (%s), with root (%s), and is ready to communicate..." % (address, root))
        except Exception as e:
            print("Could not open socket to server (%s), with root (%s), due to error (%s)" % (address, root, format(e)))
        finally: 
            self.isInitialized = True


    def SendMessage(self, message):
        while not self.isInitialized:
            continue

        if not self.isConnected:
            return

        msg = str(message.Serialize()).encode()
        print("sending message (%s) to server (%s)" % (msg, self.address))
        self.socket.send(msg)

    def run(self):
        if not self.isConnected:
            return

        self.isRunning = True
        #TODO: This fails somehow. test this properly.
        while self.isRunning:
            message = self.socket.recv(Configuration.Buffer).decode()
            print("%s received message: %s" % (self.name, str(message)))
            message = CreateOfSubType(message)
            self.parent.OnMessageReceived(self.address, message)
    
    def GetRoot(self):
        return self.root

    def GetAddress(self):
        return self.address
