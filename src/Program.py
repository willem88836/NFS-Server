
from NfsClient import *
from NfsServer import *
from ClientView import *
import time

localServer = NfsServer()
localServer.name = "ServerThread"
localServer.start()

MAX_FAILS = 3
failCount = 0


# Unsafe. Add Timeout..
while not localServer.IsActive():
    print("server is not ready yet, delaying client..")
    time.sleep(5)
    failCount += 1
    if failCount >= MAX_FAILS:
        break

## double check..    
if (failCount >= MAX_FAILS):
    print("Initializing Server failed, terminating program")
    localServer.Terminate()
else:
    clientView = ClientView()
