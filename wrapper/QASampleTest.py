import ctypes
import wrapper
import sys



lib = wrapper.loadHashLibrary(".\\bin\\windows\\hash.dll")

if __name__ == "__main__":
    # Test sample
    try: 
        wrapper.hashInit(lib)
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        if (returnCode == 0):
            ret = wrapper.waitforHashDirectory(lib, ID)
            if (ret):
                wrapper.readhashLog(lib)
                wrapper.hashStop(lib, ID)
        wrapper.hashTerminate(lib)
    except Exception as e:
        print(e)
        sys.exit("\nSystem exited with an error condition.\n")
    else:
        sys.exit("\nSystem exited successfully.\n")
