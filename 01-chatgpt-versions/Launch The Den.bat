@echo off
title The Den V6

:: Kill anything on port 8080
for /f "tokens=5" %%a in ('netstat -aon 2^>nul ^| find ":8080 "') do taskkill /f /pid %%a >nul 2>&1

:: Start The Den V6 web server (hidden)
powershell -NoProfile -Command "Start-Process python -ArgumentList '-m','http.server','8080' -WorkingDirectory 'C:\Users\Stu\Documents\Documents\AI\Claude\Code\The Den V6' -WindowStyle Hidden"

:: Wait for server to start
timeout /t 2 /nobreak >nul

:: Open The Den in Chrome
start "" "http://localhost:8080/The%%20Den.html"
