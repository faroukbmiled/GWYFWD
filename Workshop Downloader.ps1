$n = 7

$id = 2102640262

$Url = "http://workshop$n.abcvg.info/archive/431240/$id.zip"

$cpitem = "$env:userprofile\AppData\Local\Temp\$id"

$progressPreference = 'silentlyContinue'

$default = "C:\Program Files (x86)\Steam\steamapps\workshop\content\480\2335511276"

$DownloadZipFile = "$env:userprofile\AppData\Local\Temp" + $(Split-Path -Path $Url -Leaf)

$ExtractPath = "$env:userprofile\AppData\Local\Temp"

Get-ChildItem -Path $default -Include * -File -Recurse | foreach { $_.Delete()}

Invoke-WebRequest -Uri $Url -OutFile $DownloadZipFile

$ExtractShell = New-Object -ComObject Shell.Application 

$ExtractFiles = $ExtractShell.Namespace($DownloadZipFile).Items() 

$ExtractShell.NameSpace($ExtractPath).CopyHere($ExtractFiles)

Get-ChildItem -Path $cpitem -Recurse -Force |

Move-Item -destination $default -Force

Remove-Item -Path $cpitem -Recurse -Force -ErrorAction SilentlyContinue