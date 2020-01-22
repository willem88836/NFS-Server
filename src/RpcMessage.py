
class RpcMessage: 
    Type = -1
    Args = None

    def __init__(self, message):
        print("creating message")
        self.Unwrap(message)

    def Unwrap(self, message):
        print ("unwrapping message: %s" % message)
        self.Type = int(message[0:1])
        self.Args = message[1:len(message)-1]
        print(self.Type)
        
    def Wrap(self):
        # TODO: This doesn't work yet.
        wrap = self.Type + self.Args
        return wrap
