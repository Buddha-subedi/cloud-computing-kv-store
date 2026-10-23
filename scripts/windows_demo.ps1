$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
Write-Host "Make sure server is running in another terminal." -ForegroundColor Cyan
python demo.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python test_server.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python test_concurrency.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python kv_bench.py
exit $LASTEXITCODE
