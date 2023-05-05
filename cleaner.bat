@echo off

ping -n 1 localhost >nul

rem Remove RGWYFWD.exe
del RGWYFWD.exe

rem Rename RGWYFWD.exe.new to RGWYFWD.exe
ren RGWYFWD.exe.new RGWYFWD.exe

ping -n 1 localhost >nul

start RGWYFWD.exe

rem Remove self

del "%~f0"

exit /b
