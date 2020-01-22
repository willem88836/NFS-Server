import os
from tkinter.filedialog import askdirectory

Buffer = 2048
Port = 12004

ConfigPath = "~"
RootLocation = ConfigPath + "/rootPath"


# Returns the root directory of the NFS system.
# Ensures that this directory is set. 
def GetRootDirectory():
    r = ""

    if not os.path.isfile(RootLocation):
        print("root directory not set")
        if not os.path.isdir(ConfigPath):
            os.makedirs(ConfigPath)

        f = open(RootLocation, "w")
        r = askdirectory()
        f.writelines(r)
        f.close()
    else:
        print("root directory set")
        f = open(RootLocation, "r")
        r = f.read()
        f.close()

        if not os.path.isdir(r):
            print("could not find set root")
            r = askdirectory()
            f = open(RootLocation, "w")
            f.write(r)

        f.close()
    
    return r
