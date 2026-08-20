$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

# 1) Kill any existing listener on 7860 + orphan demo_app python processes
$existing = Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue
foreach ($conn in $existing) {
    Write-Host "[EM] Killing old PID $($conn.OwningProcess) on :7860"
    Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
}
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like '*demo_app*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 2

# 2) Start server detached with log capture (closing this window will NOT kill it)
$logDir = "$Root\runtime"
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }
$stdout = "$logDir\server_stdout.log"
$stderr = "$logDir\server_stderr.log"
Remove-Item $stdout, $stderr -ErrorAction SilentlyContinue

$p = Start-Process -FilePath "python" `
    -ArgumentList "-B", "demo_app\app.py" `
    -WorkingDirectory $Root `
    -WindowStyle Hidden `
    -RedirectStandardOutput $stdout `
    -RedirectStandardError $stderr `
    -PassThru

# 3) Wait up to 10s for port 7860
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    if (Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue) {
        Write-Host "[EM] OK -> http://127.0.0.1:7860 (PID $($p.Id))" -ForegroundColor Green
        Write-Host "[EM] Logs: runtime\server_stdout.log / server_stderr.log"
        Start-Process "http://127.0.0.1:7860"
        exit 0
    }
    if ($p.HasExited) { break }
}

Write-Host "[EM] FAILED to start. Last stderr:" -ForegroundColor Red
Get-Content $stderr -Tail 30
exit 1