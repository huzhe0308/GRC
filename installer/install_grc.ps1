# GRC Agent Installer
# Run: powershell -ExecutionPolicy Bypass -File install_grc.ps1

$ErrorActionPreference = "Stop"
$InstallDir = "$env:LOCALAPPDATA\GRC Agent"
$ExeName = "GRCAgent.exe"
$DesktopShortcut = "$env:USERPROFILE\Desktop\GRC Agent.lnk"
$StartMenuShortcut = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\GRC Agent.lnk"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GRC Agent - Local Client Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# --- Locate GRCAgent.exe ---
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$exePath = Join-Path $scriptDir $ExeName
if (-not (Test-Path $exePath)) {
    Write-Host "[ERROR] GRCAgent.exe not found in $scriptDir" -ForegroundColor Red
    Write-Host "Please place this installer in the same folder as GRCAgent.exe" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# --- Create install directory ---
if (Test-Path $InstallDir) {
    Write-Host "[INFO] Previous installation found at $InstallDir" -ForegroundColor Yellow
    $overwrite = Read-Host "Overwrite? (Y/n)"
    if ($overwrite -ne "" -and $overwrite.ToLower() -ne "y") {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        exit 0
    }
    Remove-Item -LiteralPath $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
New-Item -ItemType Directory -Path "$InstallDir\runtime" -Force | Out-Null
New-Item -ItemType Directory -Path "$InstallDir\runtime\reports" -Force | Out-Null
Write-Host "[OK] Install directory: $InstallDir" -ForegroundColor Green

# --- Copy exe ---
Copy-Item -LiteralPath $exePath -Destination $InstallDir -Force
Write-Host "[OK] Copied GRCAgent.exe" -ForegroundColor Green

# --- Turso credentials ---
Write-Host ""
Write-Host "Database Configuration" -ForegroundColor Cyan
Write-Host "Enter your Turso cloud database credentials." -ForegroundColor Gray
Write-Host "(Get these from Railway dashboard -> Variables)" -ForegroundColor Gray
Write-Host ""

$tursoUrl = Read-Host "TURSO_URL (libsql://xxx.turso.io)"
$tursoToken = Read-Host "TURSO_TOKEN"

if ([string]::IsNullOrWhiteSpace($tursoUrl) -or [string]::IsNullOrWhiteSpace($tursoToken)) {
    Write-Host "[WARNING] Turso credentials not provided." -ForegroundColor Yellow
    Write-Host "You can create .env manually later in: $InstallDir" -ForegroundColor Yellow
} else {
    $envContent = "TURSO_URL=$tursoUrl`nTURSO_TOKEN=$tursoToken`n"
    Set-Content -Path "$InstallDir\.env" -Value $envContent -NoNewline
    Write-Host "[OK] .env file created" -ForegroundColor Green
}

# --- Copy config files if they exist ---
foreach ($f in @("config.yaml", ".jira_config", "contacts.json")) {
    $src = Join-Path $scriptDir $f
    if (Test-Path $src) {
        Copy-Item -LiteralPath $src -Destination $InstallDir -Force
        Write-Host "[OK] Copied $f" -ForegroundColor Green
    }
}

# --- Create shortcuts ---
$shell = New-Object -ComObject WScript.Shell

# Desktop shortcut
$shortcut = $shell.CreateShortcut($DesktopShortcut)
$shortcut.TargetPath = Join-Path $InstallDir $ExeName
$shortcut.WorkingDirectory = $InstallDir
$shortcut.IconLocation = Join-Path $InstallDir $ExeName
$shortcut.Description = "GRC Agent - Local Client"
$shortcut.Save()
Write-Host "[OK] Desktop shortcut created" -ForegroundColor Green

# Start Menu shortcut
$startMenuDir = Split-Path -Parent $StartMenuShortcut
if (-not (Test-Path $startMenuDir)) {
    New-Item -ItemType Directory -Path $startMenuDir -Force | Out-Null
}
$shortcut2 = $shell.CreateShortcut($StartMenuShortcut)
$shortcut2.TargetPath = Join-Path $InstallDir $ExeName
$shortcut2.WorkingDirectory = $InstallDir
$shortcut2.IconLocation = Join-Path $InstallDir $ExeName
$shortcut2.Description = "GRC Agent - Local Client"
$shortcut2.Save()
Write-Host "[OK] Start Menu shortcut created" -ForegroundColor Green

# --- Done ---
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Install location: $InstallDir" -ForegroundColor Gray
Write-Host "Launch from: Desktop shortcut or Start Menu" -ForegroundColor Gray
Write-Host ""
$launch = Read-Host "Launch GRC Agent now? (Y/n)"
if ($launch -eq "" -or $launch.ToLower() -eq "y") {
    Start-Process -FilePath (Join-Path $InstallDir $ExeName) -WorkingDirectory $InstallDir
}
