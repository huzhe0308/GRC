@echo off
chcp 65001 >nul
echo Closing GRC Agent on port 7860...
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 7860 -State Listen -ErrorAction SilentlyContinue | ForEach-Object { Write-Host '[EM] Killing PID' $_.OwningProcess; Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }"
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*demo_app*' } | ForEach-Object { Write-Host '[EM] Killing orphan' $_.ProcessId; Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"
echo Done.
pause