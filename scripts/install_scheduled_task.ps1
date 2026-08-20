param(
    [string]$TaskName = "GRCMailWikiReport",
    [string]$At = "15:30",
    [string]$PythonPath = "python",
    [string]$ConfigPath = "D:\employee agent\config.yaml"
)

$ErrorActionPreference = "Stop"

$AgentRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Runner = Join-Path $AgentRoot "scripts\run_daily_report.py"
$WorkRoot = Split-Path -Parent $ConfigPath

if (!(Test-Path $WorkRoot)) {
    New-Item -ItemType Directory -Path $WorkRoot | Out-Null
}

$ExampleConfig = Join-Path $SkillRoot "config.example.yaml"
if (!(Test-Path $ConfigPath) -and (Test-Path $ExampleConfig)) {
    Copy-Item $ExampleConfig $ConfigPath
}

$ActionArgs = "`"$Runner`" --config `"$ConfigPath`""
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument $ActionArgs
$Trigger = New-ScheduledTaskTrigger -Daily -At $At
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 4)

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Settings $Settings -WorkingDirectory $AgentRoot -Description "Daily employee mail to automotive wiki report agent" -Force | Out-Null

Write-Host "Scheduled task installed: $TaskName"
Write-Host "Time: $At"
Write-Host "Runner: $Runner"
Write-Host "Config: $ConfigPath"
