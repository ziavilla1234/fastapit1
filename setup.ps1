param([string]$VEnvName='venv')

Write-Output '===> Settings up venv...'
py -m venv $VEnvName

$loc = Get-Location

Set-Location ".\$VEnvName\Scripts"
./Activate.ps1

Set-Location $loc
Write-Output '===> Installing packages....'
py -m pip install -r .\requirements.txt


Write-Output '===> Starting webapi srv'
uvicorn main:app