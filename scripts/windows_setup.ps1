$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
Write-Host "Installing dependencies..." -ForegroundColor Cyan
python -m pip install -r requirements.txt
Write-Host "Done. Run: .\scripts\windows_server.ps1" -ForegroundColor Green
