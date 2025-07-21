@echo off
REM === Mở Chrome debug với profile debug riêng biệt (luôn mở được port 9222) ===
set CHROME_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
set "DEBUG_PROFILE=%~dp0chrome_debug_profile"
if not exist %DEBUG_PROFILE% mkdir %DEBUG_PROFILE%
start "" %CHROME_PATH% --remote-debugging-port=9222 --user-data-dir="%DEBUG_PROFILE%"
pause 