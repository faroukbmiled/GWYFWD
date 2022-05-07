@echo off
echo GWYF Workshop Downloader by AX_Ryuk
git pull --quiet
powershell.exe -noprofile -executionpolicy bypass -file "Workshop Downloader.ps1"