# Codex and Claude Code Usage

## Codex

Codex reads [AGENTS.md](../AGENTS.md) as the root operating guide for this repository.

Recommended pattern:

1. Create a task with `scripts/sansheng.py create`.
2. Draft a Zhongshu plan before editing files.
3. Let Menxia review the plan. If the plan has gaps, fix the plan first.
4. Dispatch execution work to the appropriate ministry roles.
5. Record every meaningful result with `todo`, `progress`, and `flow`.
6. Produce the final answer from `report`.

When Codex has no real subagent facility in the current runtime, simulate agents as sequential role passes. The important invariant is that planning, review, execution, and synthesis remain separate.

## Claude Code

Claude Code subagents are stored in [.claude/agents](../.claude/agents).

Typical usage:

- Ask `zhongshu` to draft the plan.
- Ask `menxia` to review it.
- Ask `shangshu` to route work.
- Use `bingbu`, `xingbu`, `libu`, `hubu`, `gongbu`, and `libu_hr` for concrete work.

Each subagent prompt intentionally stays short. The canonical responsibilities live in [agents](../agents), and the workflow contract lives in [AGENTS.md](../AGENTS.md).

## Shared CLI

Both Codex and Claude Code should use the same CLI:

```bash
python scripts/sansheng.py doctor
python scripts/sansheng.py next <task-id>
python scripts/sansheng.py report <task-id>
```

This keeps task history independent from the model host.

