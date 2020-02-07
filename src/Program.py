
from NfsClient import *
from NfsServer import *
from ClientView import *
import time

localServer = NfsServer()
localServer.name = "ServerThread"
localServer.start()

MAX_FAILS = 3
SLEEP_DURATION = 5
failCount = 0

serverFailed = False

while not localServer.IsActive():
    print("server is not ready yet, delaying client..")
    time.sleep(SLEEP_DURATION)
    failCount += 1
    if failCount >= MAX_FAILS:
        serverFailed = True
        break

if (serverFailed):
    print("Initializing Server failed, terminating program")
    localServer.Terminate()
else:
    clientView = ClientView()
