param(
    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Source = Join-Path $RepoRoot "skills\sansheng-liubu"

if (-not (Test-Path (Join-Path $Source "SKILL.md"))) {
    throw "Canonical skill not found: $Source"
}

$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
$Targets = @(
    (Join-Path $RepoRoot ".claude\skills\sansheng-liubu"),
    (Join-Path $CodexHome "skills\sansheng-liubu"),
    (Join-Path $env:USERPROFILE ".claude\skills\omc-learned\sansheng-liubu")
)

function Copy-Skill {
    param(
        [string]$Target
    )

    Write-Output "sync $Source -> $Target"

    if ($DryRun) {
        return
    }

    if ((Test-Path $Target) -and -not $Force) {
        $answer = Read-Host "Overwrite existing target? $Target [y/N]"
        if ($answer -notin @("y", "Y", "yes", "YES")) {
            Write-Output "skip $Target"
            return
        }
    }

    $parent = Split-Path -Parent $Target
    New-Item -ItemType Directory -Force -Path $parent | Out-Null

    if (Test-Path $Target) {
        Remove-Item -LiteralPath $Target -Recurse -Force
    }

    Copy-Item -LiteralPath $Source -Destination $Target -Recurse -Force
}

foreach ($target in $Targets) {
    Copy-Skill -Target $target
}

Write-Output "done"
