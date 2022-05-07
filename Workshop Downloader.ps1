$Url = "http://workshop7.abcvg.info/archive/431240/1475634610.zip"

$cpitem = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480\1475634610"

$default = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480\2335511276"

$DownloadZipFile = "C:\Program Files (x86)\Steam\steamapps\workshop\content\" + $(Split-Path -Path $Url -Leaf)

$ExtractPath = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480"

Invoke-WebRequest -Uri $Url -OutFile $DownloadZipFile

$ExtractShell = New-Object -ComObject Shell.Application 

$ExtractFiles = $ExtractShell.Namespace($DownloadZipFile).Items() 

$ExtractShell.NameSpace($ExtractPath).CopyHere($ExtractFiles)

Get-ChildItem -Path $cpitem -Recurse -Force |
  Where-Object {$_.LastWriteTime -lt (Get-date).AddDays(-31)} |
  Move-Item -destination $default -Force