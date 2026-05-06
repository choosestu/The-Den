@echo off
REM Den Evening Check — runs at 7pm via Windows Task Scheduler
REM Opens The Den if not already open, triggering the auto Drive/Fieldy check

REM Check if server is running on 8080
netstat -ano | find ":8080 " >nul 2>&1
if errorlevel 1 (
    REM Server not running — start it
    cd /d "C:\Users\Stu\Documents\Documents\AI\ChatGPT"
    start /min "The Den Server" cmd /k python -m http.server 8080
    timeout /t 3 /nobreak >nul
)

REM Open The Den in Chrome (will auto-check Drive at 7pm on load)
start "" "http://localhost:8080/The%%20Den.html"
