import ctypes
from wrapper import wrapper
import pytest
import os
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

def test_hash_stoped_twice(cleanup):
       # Verify that hashStop stopped specific ID and error is returned when it's called 2nd time
       wrapper.hashInit(lib)
       returnCode, ID = wrapper.hashDirectory(lib, ".")
       if (returnCode == 0):
                ret = wrapper.waitforHashDirectory(lib, ID)
                returnCode = wrapper.hashStop(lib, ID)
                assert returnCode == 0
                returnCode = wrapper.hashStop(lib, ID)
                assert returnCode == 5

def test_hash_terminated_twice(cleanup):
       # Verify that hashTerminate does really terminate the library and error is returned when it's called 2nd time
        wrapper.hashInit(lib)
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        if (returnCode == 0):
                ret = wrapper.waitforHashDirectory(lib, ID)
        returnCode = wrapper.hashTerminate(lib)
        assert returnCode == 0
        returnCode = wrapper.hashTerminate(lib)
        assert returnCode == 7

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
        assert returnCode == 0
        if (returnCode == 0):
            ret = wrapper.waitforHashDirectory(lib, ID)
            if (ret):
                storelogbit = wrapper.hashedfiles(lib)
                storedlogs = wrapper.filesInDirectory(storelogbit)
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

def test_hash_read_next_log_line_with_empty_directory(cleanup):
        # Verify error code of hashReadNextLogLine with empty repository
        os.chdir('.\\test')
        lib = wrapper.loadHashLibrary("..\\bin\\windows\\hash.dll")
        wrapper.hashInit(lib)
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        assert returnCode ==0
        if (returnCode == 0):
            ret = wrapper.waitforHashDirectory(lib, ID)
            if (ret):
                returnCode, logline = wrapper.hashReadNextLogLine(lib)
                assert returnCode == 1
        os.chdir('..\\')

def test_hash_file_with_space_and_without_format(cleanup):
        # Verify that hash can work with space and no format
        file_name = "test_file"
        with open(file_name, "w") as f:
                f.write("This is a pytest test file.")
        wrapper.hashInit(lib)
        expected = wrapper.expectedFiles (".")
        assert file_name in expected 
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        if (returnCode == 0):
            ret = wrapper.waitforHashDirectory(lib, ID)
            if (ret):
                storelogbit = wrapper.hashedfiles(lib)
                storedlogs = wrapper.filesInDirectory(storelogbit)
                for i in range(len(expected)):
                     assert expected[i] == storedlogs[i]              
                wrapper.hashStop(lib, ID)
        wrapper.hashTerminate(lib)
        if os.path.exists(file_name):
                os.remove(file_name)

def test_hash_file_with_special_character_and_number(cleanup):
        # Verify that hash can work with special characters and number
        file_name = "ahoj+!#$%^&(){};'[]=-0"
        with open(file_name, "w") as f:
                f.write("This is a pytest test file.")
        wrapper.hashInit(lib)
        expected = wrapper.expectedFiles (".")
        assert file_name in expected 
        returnCode, ID = wrapper.hashDirectory(lib, ".")
        if (returnCode == 0):
            ret = wrapper.waitforHashDirectory(lib, ID)
            if (ret):
                storelogbit = wrapper.hashedfiles(lib)
                storedlogs = wrapper.filesInDirectory(storelogbit)
                for i in range(len(expected)):
                     assert expected[i] == storedlogs[i]              
                wrapper.hashStop(lib, ID)
        wrapper.hashTerminate(lib)
        if os.path.exists(file_name):
                os.remove(file_name)

def test_multiple_operation_id(cleanup):
        # Verify operation ids are alocated correctly
        wrapper.hashInit(lib)
        for i in range(50):
            returnCode, ID = wrapper.hashDirectory(lib, ".")
            assert ID == i+1     
