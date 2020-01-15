

class RpcMessage: 
    def __init__(self, message):
        print("creating message")
        self.Unwrap(message)

    def Unwrap(self, message):
        print ("unwrapping message: %s" % message)

    def Wrap(self):
        print("Wrappign message")


