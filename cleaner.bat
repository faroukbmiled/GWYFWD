@echo off

rem Kill any process running RGWYFWD.exe
taskkill /f /im RGWYFWD.exe

timeout /t 1 /nobreak >nul

del RGWYFWD.exe

ren RGWYFWD.exe.new RGWYFWD.exe

rem Ping localhost to give the OS time to finish killing the process
ping /n 1 /w 1000 localhost >nul

rem Start RGWYFWD.exe
start RGWYFWD.exe

rem Remove self
del "%~f0"

exit /b
