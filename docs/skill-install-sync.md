# Skill Install and Sync

This repository keeps `skills/sansheng-liubu/` as the canonical source.

Use the sync helper from the repo root:

```powershell
.\scripts\sync-sansheng-skill.ps1 -DryRun
.\scripts\sync-sansheng-skill.ps1
```

## Targets

The helper syncs the canonical skill to:

- repo-local Claude project skill: `.claude/skills/sansheng-liubu`
- Codex user skill: `$CODEX_HOME\skills\sansheng-liubu`, or `%USERPROFILE%\.codex\skills\sansheng-liubu` when `CODEX_HOME` is unset
- Claude learned skill: `%USERPROFILE%\.claude\skills\omc-learned\sansheng-liubu`

It also leaves the thin Claude command and role adapters in this repository:

- `.claude/commands/sansheng.md`
- `.claude/agents/*.md`

## Verification

After syncing:

```powershell
Test-Path "$env:USERPROFILE\.codex\skills\sansheng-liubu\SKILL.md"
Test-Path "$env:USERPROFILE\.claude\skills\omc-learned\sansheng-liubu\SKILL.md"
powershell -ExecutionPolicy Bypass -File .\tests\skill-static-check.ps1
```

Then start a new Codex or Claude Code session so the tools rescan available skills.
