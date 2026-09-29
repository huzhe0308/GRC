# GRC Agent Uninstaller
$ErrorActionPreference = "Stop"
$InstallDir = "$env:LOCALAPPDATA\GRC Agent"
$DesktopShortcut = "$env:USERPROFILE\Desktop\GRC Agent.lnk"
$StartMenuShortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\GRC Agent.lnk"

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  GRC Agent - Uninstaller" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Remove GRC Agent? This will delete all local data. (y/N)"
if ($confirm.ToLower() -ne "y") {
    Write-Host "Uninstall cancelled." -ForegroundColor Gray
    exit 0
}

# Kill running process
Get-Process -Name "GRCAgent" -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 1

# Remove shortcuts
Remove-Item -LiteralPath $DesktopShortcut -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $StartMenuShortcut -Force -ErrorAction SilentlyContinue
$startMenuDir = Split-Path -Parent $StartMenuShortcut
if ((Get-ChildItem $startMenuDir -ErrorAction SilentlyContinue | Measure-Object).Count -eq 0) {
    Remove-Item -LiteralPath $startMenuDir -Force -ErrorAction SilentlyContinue
}
Write-Host "[OK] Shortcuts removed" -ForegroundColor Green

# Remove install directory
if (Test-Path $InstallDir) {
    Remove-Item -LiteralPath $InstallDir -Recurse -Force
    Write-Host "[OK] Install directory removed: $InstallDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "GRC Agent has been uninstalled." -ForegroundColor Green
Read-Host "Press Enter to exit"
