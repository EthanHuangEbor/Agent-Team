$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Skill = Join-Path $RepoRoot "skills\sansheng-liubu"
$SkillMd = Join-Path $Skill "SKILL.md"
$OpenAi = Join-Path $Skill "agents\openai.yaml"
$ClaudeCommand = Join-Path $RepoRoot ".claude\commands\sansheng.md"
$ClaudeAgents = Join-Path $RepoRoot ".claude\agents"

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message
    )
    if (-not $Condition) {
        throw $Message
    }
}

function Read-Utf8 {
    param([string]$Path)
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

Assert-True (Test-Path $SkillMd) "Missing canonical skill SKILL.md"
Assert-True (Test-Path $OpenAi) "Missing agents/openai.yaml"
Assert-True (Test-Path $ClaudeCommand) "Missing Claude /sansheng command"
Assert-True (Test-Path $ClaudeAgents) "Missing Claude agents directory"

$skillText = Read-Utf8 $SkillMd
Assert-True ($skillText -match "(?s)^---\s*name:\s*sansheng-liubu\s*description:.*?---") "SKILL.md frontmatter must contain only name and description"
Assert-True ($skillText -match "two-round|两轮|two repair rounds") "SKILL.md must define two-round iteration"
Assert-True ($skillText -match "subagent|multi-agent|role passes") "SKILL.md must define delegation behavior"

$openAiText = Read-Utf8 $OpenAi
Assert-True ($openAiText.Contains('$sansheng-liubu')) "openai.yaml default_prompt must mention `$sansheng-liubu"

$commandText = Read-Utf8 $ClaudeCommand
Assert-True ($commandText.Contains("sansheng-liubu")) "Claude command must invoke sansheng-liubu"
Assert-True ($commandText.Length -lt 600) "Claude command must stay thin"

$agentText = Get-ChildItem -Path $ClaudeAgents -Filter "*.md" | ForEach-Object { Read-Utf8 $_.FullName } | Out-String
foreach ($forbidden in @("scripts/sansheng.py", "tasks.json", "events.jsonl", "task ledger", "任务账本", "JJC-")) {
    Assert-True (-not $agentText.Contains($forbidden)) "Claude agents still reference old ledger term: $forbidden"
}

$mainFiles = @(
    "README.md",
    "AGENTS.md",
    "docs\architecture.md",
    "docs\codex-claude-code.md",
    "docs\output-contract.md",
    "docs\skill-install-sync.md",
    "examples\sample-edict.md"
)

$mainText = $mainFiles | ForEach-Object { Read-Utf8 (Join-Path $RepoRoot $_) } | Out-String
foreach ($forbidden in @("scripts/sansheng.py", "tasks.json", "events.jsonl", "JJC-")) {
    Assert-True (-not $mainText.Contains($forbidden)) "Main docs still recommend old flow term: $forbidden"
}

foreach ($required in @(
    "references\workflow-contract.md",
    "references\role-map.md",
    "references\self-iteration.md",
    "references\output-contract.md",
    "references\claude-code-adapter.md",
    "references\examples.md"
)) {
    Assert-True (Test-Path (Join-Path $Skill $required)) "Missing skill reference: $required"
}

Write-Output "skill static check ok"
