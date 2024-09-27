import ctypes
from wrapper import wrapper
import pytest
# Load the hash library depending on the platform
lib = ctypes.cdll.LoadLibrary('.\\bin\\windows\\hash.dll')

@pytest.fixture
def cleanup():
        wrapper.hashTerminate(lib)
        yield
        

def test_has_init(cleanup):
        # Verify that hash initialization is successfull 
        returnCode = wrapper.hashInit(lib)
        assert returnCode == 0

def test_hash_init_terminate(cleanup):
        # Verify that hash initialization and termination is sucesfull
        returnCode = wrapper.hashInit(lib)
        assert returnCode == 0
        returnCode = wrapper.hashTerminate(lib)
        assert returnCode == 0

def test_hash_init_already_initialized(cleanup):
        # Verify that hashInit cannot be initialized when it's already initialized
        returnCode = wrapper.hashInit(lib)
        assert returnCode == 0
        returnCode = wrapper.hashInit(lib)
        assert returnCode == 8

def test_hash_directory_null(cleanup):
        # Test hashDirectory with None as path
        returnCode = wrapper.hashInit(lib)
        assert returnCode == 0
        returnCode, ID = wrapper.hashDirectory(lib, None)
        assert returnCode == 6        

def test_correct_files_hashed(cleanup):
        # Verification that hash workflow works as expected and correct files are hashed 
        wrapper.hashInit(lib)
        expected = wrapper.expectedFiles (".")
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        if (returnCode == 0):
            ret = wrapper.waitforHashDirectory(lib, ID)
            if (ret):
                storelogbit = wrapper.hashedfiles(lib)
                storedlogs = wrapper.filesInDirectory(storelogbit)
                wrapper.readhashLog(lib)
                for i in range(len(expected)):
                     assert expected[i] == storedlogs[i]                
                returnCode = wrapper.hashStop(lib, ID)
                assert returnCode == 0
        returnCode = wrapper.hashTerminate(lib)
        assert returnCode == 0
        
def test_without_init(cleanup):
        # Test Sample without hash initialization
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        assert returnCode == 7
        if (returnCode == 7):
                returnCode = wrapper.hashStop(lib, ID)
                assert returnCode == 5 # possible bug.
        returnCode = wrapper.hashTerminate(lib)
        assert returnCode ==7

def test_hash_read_next_log_line_without_init(cleanup):
        # Verify error code of hashReadNextLogLine without hasInit
        returnCode, logline = wrapper.hashReadNextLogLine(lib)
        assert returnCode == 7

def test_hash_read_next_log_line_with_init(cleanup):
        # Verify error code of hashReadNextLogLine with only hasInit
        wrapper.hashInit(lib)
        returnCode, logline = wrapper.hashReadNextLogLine(lib)
        assert returnCode == 1

def test_multiple_operation_id(cleanup):
        # Verify operation ids are alocated correctly
        wrapper.hashInit(lib)
        for i in range(50):
            returnCode, ID = wrapper.hashDirectory(lib, ".")
            assert ID == i+1     
