@echo off

echo =======================
echo [INFO] Terminating python.exe process...
taskkill /F /IM python.exe
IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] python.exe process has been terminated.
) ELSE (
    echo [ERROR] Failed to terminate python.exe process.
)

echo =======================
echo [INFO] Terminating fiftyone.exe process...
taskkill /F /IM fiftyone.exe
IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] fiftyone.exe process has been terminated.
) ELSE (
    echo [ERROR] Failed to terminate fiftyone.exe process.
)

echo =======================
echo [INFO] Terminating mongod.exe process...
taskkill /F /IM mongod.exe
IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] mongod.exe process has been terminated.
) ELSE (
    echo [ERROR] Failed to terminate mongod.exe process.
)

echo =======================
echo [INFO] Deleting Mongo database folder...
rd /s /q "C:\Users\Administrator\.fiftyone\var\lib\mongo"
IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Mongo database folder has been deleted.
) ELSE (
    echo [ERROR] Failed to delete Mongo database folder.
)

echo =======================
pause
