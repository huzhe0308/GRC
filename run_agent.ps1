param(
    [switch]$Force,
    [ValidateSet("api", "codex_assisted")]
    [string]$Mode = ""
)

$ErrorActionPreference = "Stop"
$AgentRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = Join-Path $AgentRoot "config.yaml"
$Runner = Join-Path $AgentRoot "scripts\run_daily_report.py"

$arguments = @($Runner, "--config", $ConfigPath)
if ($Force) {
    $arguments += "--force"
}
if ($Mode) {
    $arguments += @("--mode", $Mode)
}

Push-Location $AgentRoot
try {
    & python @arguments
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
