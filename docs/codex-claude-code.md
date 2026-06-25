# Codex and Claude Code Usage

## Codex

Install or copy the skill into `~/.codex/skills/sansheng-liubu`, then invoke:

```text
Use $sansheng-liubu to handle this task with 三省六部, dispatch relevant ministries, self-review twice at most, and return the final memorial.
```

Codex should read `skills/sansheng-liubu/SKILL.md` and then load referenced files only when needed.

## Claude Code

Claude Code has three adapters:

- Project skill: `.claude/skills/sansheng-liubu/SKILL.md`
- Slash command: `.claude/commands/sansheng.md`
- Role adapters: `.claude/agents/*.md`

Use:

```text
/sansheng <your task>
```

The slash command is intentionally thin. It invokes the skill and does not duplicate the workflow.

## Subagent Behavior

When real subagents are available, use them for concrete non-overlapping offices or ministries. When unavailable, run explicit labeled role passes. In both cases, Menxia approval is required before Shangshu dispatch.

