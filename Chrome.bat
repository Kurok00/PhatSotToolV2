@echo off
setlocal

REM === Tìm kiếm Chrome ở các vị trí phổ biến ===
set CHROME_PATH=
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" set CHROME_PATH=%ProgramFiles%\Google\Chrome\Application\chrome.exe
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" set CHROME_PATH=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" set CHROME_PATH=%LocalAppData%\Google\Chrome\Application\chrome.exe
if exist "%UserProfile%\AppData\Local\Google\Chrome\Application\chrome.exe" set CHROME_PATH=%UserProfile%\AppData\Local\Google\Chrome\Application\chrome.exe

if "%CHROME_PATH%"=="" (
    echo Không tìm thấy Chrome! Vui lòng cài đặt Google Chrome.
    timeout /t 5
    exit /b
)

REM === Mở Chrome debug với profile mặc định, port 9222 ===
start "" "%CHROME_PATH%" --remote-debugging-port=9222 --user-data-dir="%cd%\chrome_debug_profile" --profile-directory="Default"
exit 