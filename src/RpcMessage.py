
class RpcMessage: 
    Type = None
    Args = None

    def __init__(self, t, args):
        print("creating message")
        self.Type = t
        self.Args = args

    def Unwrap(self, message):
        print ("unwrapping message: %s" % message)
        self.Type = int(message[0:1])
        self.Args = message[1:len(message)]
        print(self.Type)
        
    def Wrap(self):
        # TODO: This doesn't work yet.
        wrap = self.Type + self.Args
        return wrap
