# Agent-Team

一个面向 Codex / Claude Code 的 **三省六部制 skill-first 多 agent 协作系统**。

本仓库不再以外部状态 CLI 为核心。核心入口是 [`skills/sansheng-liubu/SKILL.md`](skills/sansheng-liubu/SKILL.md)：在 Codex 中调用 `$sansheng-liubu`，或在 Claude Code 中调用 `/sansheng`，即可按太子分拣、中书拟案、门下审议、尚书派发、六部执行、刑部复核、最终回奏的制度完成复杂任务。

## Quick Start

Codex:

```text
Use $sansheng-liubu to decompose this goal, dispatch the ministries, self-review twice at most, and return the final memorial.
```

Claude Code:

```text
/sansheng 为这个仓库建立发布检查清单，并自审查两轮封顶
```

安装到本机 skill 目录：

```powershell
.\scripts\sync-sansheng-skill.ps1 -DryRun
.\scripts\sync-sansheng-skill.ps1
```

详细说明见 [docs/skill-install-sync.md](docs/skill-install-sync.md)。

## What It Does

`sansheng-liubu` skill 将复杂任务变成一套可执行的 agent 协作制度：

1. **太子**：分拣请求，提炼标题、目标、约束和交付物。
2. **中书省**：拟定方案、拆解任务、定义验收标准。
3. **门下省**：按可行性、完整性、风险、资源四项强制审议，可准奏或封驳。
4. **尚书省**：只在准奏后派发六部，并综合结果。
5. **六部**：兵部实现、刑部验收、礼部文档、户部数据、工部部署、吏部 agent/流程。
6. **自迭代**：门下或刑部发现问题时最多修正两轮；第二轮仍不通过则停止并回奏风险。

有真实 subagent / multi-agent 工具时，skill 要求按职责派发；没有工具时，用明确标注的角色 pass 模拟同一制度。

## Repository Layout

```text
skills/sansheng-liubu/       Canonical Codex/Claude skill package
  SKILL.md                   Trigger metadata and core workflow
  agents/openai.yaml         Codex UI metadata
  references/                Workflow, role map, iteration, output contracts

.claude/skills/sansheng-liubu/  Claude project skill adapter
.claude/commands/sansheng.md    Claude slash command alias
.claude/agents/                 Claude role adapters
docs/                           Architecture and install/sync docs
scripts/sync-sansheng-skill.ps1 Idempotent local sync helper
tests/skill-static-check.ps1    Static acceptance checks
```

## Validation

```powershell
powershell -ExecutionPolicy Bypass -File .\tests\skill-static-check.ps1
python C:\Users\Lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\sansheng-liubu
```

The static check verifies that:

- the canonical skill exists;
- `openai.yaml` points to `$sansheng-liubu`;
- Claude `/sansheng` exists and stays thin;
- Claude agents no longer reference the old state CLI;
- main docs no longer recommend the old CLI flow.

## Design Notes

- Inspired by [cft0808/edict](https://github.com/cft0808/edict), but implemented as a portable skill rather than a service or task database.
- The skill is the single source of truth. Claude commands and agents are adapters, not separate workflows.
- Python ledger code from the previous implementation was removed from the main path because it conflicted with the desired Codex/Claude native invocation model.
