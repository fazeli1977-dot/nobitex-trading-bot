@echo off
setlocal

for /f "tokens=2 delims==" %%P in ('wmic process where "name='cmd.exe'" get commandline /value ^| findstr /i "Nobitex Trading Bot" 2^>nul') do (
    set PROCESS_CMD=%%P
)

if defined PROCESS_CMD (
    taskkill /F /IM cmd.exe /FI "WINDOWTITLE eq Nobitex Trading Bot" >nul 2>&1
    echo Graceful shutdown request sent.
) else (
    echo Bot process is not running.
)

exit /b 0
