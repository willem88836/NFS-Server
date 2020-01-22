
class RpcMessage: 
    Type = -1
    Content = None

    def __init__(self, message):
        print("creating message")
        self.Unwrap(message)

    def Unwrap(self, message):
        print ("unwrapping message: %s" % message)
        self.Type = int(message[0:1])
        self.Content = message[1:len(message)-1]
        print(self.Type)
        
    def Wrap(self):
        # TODO: This doesn't work yet.
        wrap = self.Type + self.Content
        return wrap

class RpcMessageType:
    ExceptionOccurred = 0
    RequestFileAccess = 1
    ReleaseFileAccess = 2
    RequestFileUpdate = 3
