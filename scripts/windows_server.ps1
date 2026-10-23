$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
Write-Host "Starting KV server at http://127.0.0.1:8080" -ForegroundColor Cyan
python -u server.py
