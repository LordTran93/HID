# Bug Summary Report

This document provides an overview of the bugs detected during testing of the application. 

## Bug Details

### 001: HASH_ERROR_ALREADY_INITIALIZED message is not returned when it's already initialized
- **Steps to Reproduce**:
  1. Initialize hash
  2. Verify that Code 0 (HASH_ERROR_OK) is returned
  3. Initialize hash again
- **Expected Result**: Returned Code is 8 (HASH_ERROR_ALREADY_INITIALIZED)

- **Acual Result**: Returned Code 0 (HASH_ERROR_OK) is returned
```bash
returnCode = wrapper.hashInit(lib)
assert returnCode == 0
returnCode = wrapper.hashInit(lib)
assert returnCode == 8
```
---

### 002: hashStop ends in loop when it's executed right after hashDirectory
- **Steps to Reproduce**:
  1. Initialize hash
  2. run hashDirectory(lib, ".")
  3. run hashStop(lib, ID)
- **Expected Result**: Returned Code is 0 (HASH_ERROR_OK)

- **Acual Result**: Application ends up in loop
```bash
wrapper.hashInit(lib)
returnCode, ID = wrapper.hashDirectory(lib, ".")
wrapper.hashStop(lib, ID)
```
---

### 004: hashTerminate ends in loop when it's executed right after hashDirectory
- **Steps to Reproduce**:
  1. Initialize hash
  2. run hashDirectory(lib, '.')
  3. run hashTerminate(lib)
- **Expected Result**: Returned Code is 0 (HASH_ERROR_OK)

- **Acual Result**: Application ends up in loop
```bash
wrapper.hashInit(lib)
wrapper.hashDirectory(lib, ".")
wrapper.hashTerminate(lib)
```
---

### 005: hashDirectory is able to run only in current directory
- **Steps to Reproduce**:
  1. Initialize hash
  2. Run hashDirectory with directory '.\\wrapper\\' or full path of other directory than current ('.')
  3. Read hashReadNextLogLine
- **Expected Result**: files with hash are returned

- **Acual Result**: hashReadNextLogLine doesn't return anything
```bash
wrapper.hashInit(lib)
returnCode, ID = wrapper.hashDirectory(lib, ".\\wrapper\\")
if (returnCode == 0):
    ret = wrapper.waitforHashDirectory(lib, ID)
    if (ret):
        wrapper.readhashLog(lib)
        returnCode = wrapper.hashStop(lib, ID)
        assert returnCode == 0
returnCode = wrapper.hashTerminate(lib)
assert returnCode == 0
```
---

### 006: Possible bug with hashStop when hash is not initialized
- **Steps to Reproduce**:
  1. run hashStop(lib, 1)
- **Expected Result**: Error Code 7 (HASH_ERROR_NOT_INITIALIZED) is returned

- **Acual Result**: Error Code 5 (HASH_ERROR_ARGUMENT_INVALID) is returned. Both Error Codes make sense but it's not clear from hash.h which one is expected
```bash
returnCode = wrapper.hashStop(lib, ID)
assert returnCode == 7
```
---

### 007: Possible bug with hashStop when hash is not initialized
- **Steps to Reproduce**:
  1. run hashStop(lib, 1)
- **Expected Result**: Error Code 7 (HASH_ERROR_NOT_INITIALIZED) is returned

- **Acual Result**: Error Code 5 (HASH_ERROR_ARGUMENT_INVALID) is returned. Both Error Codes make sense but it's not clear from hash.h which one is expected
```bash
returnCode = wrapper.hashStop(lib, ID)
assert returnCode == 7
```
---
### 008: Filename with non-ASCII characters causing crash
- **Steps to Reproduce**:
  1. Add file with non-ASCII character (€, ㅂ, á )
- **Expected Result**: Hashdirectory is successful or proper Error Code should be returned

- **Acual Result**: Application unexpectly crash. Following error was found in log
```bash
  File "C:\Users\tran4\Desktop\HID QA HomeworkV2 Helper\wrapper\wrapper.py", line 82 in hashStatus
  File "CWindows fatal exception: access violation
```
---

### 009: Hashing large files causing crash
- **Steps to Reproduce**:
  1. Add large file into repository (2GB in my case)
  2. hasInit
  3. hashDirectory with large file

  - **Steps to Reproduce**:
  1. Add large file into repository (200MB in my case)
  2. hasInit
  3. hashDirectory in loop (20)

- **Expected Result**: Hashdirectory is successful

- **Acual Result**: Application unexpectly crash. Following error was found in log. Issue is probably Memory related but can't tell based logs whether issue is with pyhton or library
```bash
Fatal Python error: Aborted
```
---