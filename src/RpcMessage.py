
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
        #TODO: This code looks evil. I don't like that. Improve this.
        msg = str(message[1:len(message)-1])
        self.Type = int(msg[0])
        self.Args = msg[3:len(msg)]
        
    def Wrap(self):
        wrap = [self.Type, self.Args]
        return wrap
