
class RpcMessage: 
    Type = None
    Args = None

    def __init__(self, t, args, wrapped = None):
        if (wrapped != None):
            self.Unwrap(wrapped)
        else:
            self.Type = t
            self.Args = args

    def Unwrap(self, message):
        self.Type = int(message[0:1])
        self.Args = message[1:len(message)]
        
    def Wrap(self):
        wrap = [self.Type, self.Args]
        return wrap
