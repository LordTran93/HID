#
# IMPORTANT: To load 32-bit DLL, use 32-bit Python!
#
import ctypes
import time
import os

ReturnCodes = {
    0: 'HASH_ERROR_OK',
    1: 'HASH_ERROR_GENERAL',
    2: 'HASH_ERROR_EXCEPTION',
    3: 'HASH_ERROR_MEMORY',
    4: 'HASH_ERROR_LOG_EMPTY',
    5: 'HASH_ERROR_ARGUMENT_INVALID',
    6: 'HASH_ERROR_ARGUMENT_NULL',
    7: 'HASH_ERROR_NOT_INITIALIZED',
    8: 'HASH_ERROR_ALREADY_INITIALIZED'
}


def loadHashLibrary(libFullPath):
    try:
        lib = ctypes.cdll.LoadLibrary(libFullPath)
    except FileNotFoundError as e:
        print("Library file not found.")
        raise e
    except OSError as e:
        print("Library cannot be loaded. System will exit without calling the hash routines.")
        raise e
    except Exception as e:
        print(e)
        raise e
    else:
        print("\nLibrary loaded successfully.")
        return lib


def hashInit(library):
    returnCode = library.HashInit()
    print('\nHashInit Return code: {}.'.format(ReturnCodes[returnCode]))
    return returnCode


def hashTerminate(library):
    returnCode = library.HashTerminate()
    print('\nHashTerminate Return code: {}.'.format(ReturnCodes[returnCode]))
    return returnCode  


def hashDirectory(library, directoryFullPath):
    opID = ctypes.c_size_t(0)

    returnCode = library.HashDirectory(ctypes.c_wchar_p(directoryFullPath), ctypes.byref(opID))
    print('\nHashDirectory Return code: {}, Operation ID: {}.'.format(ReturnCodes[returnCode], opID.value))
    return returnCode, int(opID.value)


def hashReadNextLogLine(library):
    HASHLENGTHINBYTE = 64
    HashFunction = library.HashReadNextLogLine
    HashFunction.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    
    logLine = ctypes.c_char_p()
    buffer = (ctypes.c_char * (HASHLENGTHINBYTE + 1))()
    returnCode = library.HashReadNextLogLine(ctypes.byref(logLine))
    if (returnCode == 0):
        ctypes.memmove(buffer, logLine, (HASHLENGTHINBYTE + 1))
        library.HashFree(logLine)

    #When returnCode is 0 ('HASH_ERROR_OK'), buffer contains w_char array terminated by a null character
    return returnCode, buffer.value


def hashStop(library, opID):
    returnCode = library.HashStop(ctypes.c_size_t(opID))
    print('\nHashStop Return code: {}.'.format(ReturnCodes[returnCode]))
    return returnCode  


def hashStatus(library, opID):
    opRunning = ctypes.c_bool(False)
    returnCode = library.HashStatus(ctypes.c_size_t(opID), ctypes.byref(opRunning))
    return returnCode, bool(opRunning)

            
  
def readhashLog(library):
    print('')
    while True:
        returnCode, logLine = hashReadNextLogLine(library)
        if (int(returnCode) == 0): 
            print(logLine)
        else:
            break
    return 


def waitforHashDirectory(library, opID:int):
    while True:
        returnCode, opRunning = hashStatus(library, opID)
        if ((int(returnCode) != 0) or (opRunning != True)): 
            print('\nHashStatus Return code: {}.'.format(ReturnCodes[returnCode]))
            break
    print('\nHashDirectory has finished.')
    return True

def expectedFiles (directoryFullPath):
        expected_files =[]
        for filename in os.listdir(directoryFullPath):
            if os.path.isfile(os.path.join(directoryFullPath, filename)):
                expected_files.append(filename)
        return expected_files

def hashedfiles(library):
        storelogbit = []
        while True:
            returnCode, logLine = hashReadNextLogLine(library)
            if (int(returnCode) == 0): 
                storelogbit.append(logLine)
            else:
                break           
        return storelogbit

def filesInDirectory(storelogbit):
        files = []
        for i in storelogbit:
            decoded_string = i.decode('utf-8')
            cleared_string = decoded_string.replace('1 .\\','')
            file_name = cleared_string.rsplit(' ',1)[0]
            files.append(file_name)
        return files

def hashFree(library):
    freeMemory = library.HashFree()
    freeMemory.argtypes  = [ctypes.c_void_p]
    freeMemory.restype = None