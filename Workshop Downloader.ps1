Invoke-WebRequest -Uri $Url -OutFile $DownloadZipFile

$Url = "http://workshop2.abcvg.info/archive/431240/1415958558.zip"

$cpitem = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480\1415958558"

$default = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480\2335511276"

$DownloadZipFile = "C:\Program Files (x86)\Steam\steamapps\workshop\content\" + $(Split-Path -Path $Url -Leaf)

$ExtractPath = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480"

$ExtractShell = New-Object -ComObject Shell.Application 

$ExtractFiles = $ExtractShell.Namespace($DownloadZipFile).Items() 

$ExtractShell.NameSpace($ExtractPath).CopyHere($ExtractFiles)

Get-ChildItem -Path $cpitem -Recurse -Force |
  Where-Object {$_.LastWriteTime -lt (Get-date).AddDays(-31)} |
  Move-Item -destination $default -Force