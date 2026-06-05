@echo off
echo Cleaning active processes on port 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do (
    echo Terminating conflicting PID %%a...
    taskkill /F /PID %%a 2>nul
)
echo Starting local HTTP server on port 8000...
pushd portal
python -m http.server 8000
popd
