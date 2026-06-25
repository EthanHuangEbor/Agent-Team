# Claude Code Adapter

Claude Code should use the same canonical skill rules as Codex.

## Invocation

- Primary project skill: `.claude/skills/sansheng-liubu/SKILL.md`.
- Convenience command: `.claude/commands/sansheng.md`.
- Subagents: `.claude/agents/*.md`.

The slash command should stay thin and should not duplicate the full workflow. It should tell Claude to use the `sansheng-liubu` skill for the supplied arguments.

## Agent Adapters

Claude subagents are role adapters:

- `taizi`: intake and normalized brief.
- `zhongshu`: plan only.
- `menxia`: review gate only.
- `shangshu`: dispatch and synthesis.
- `bingbu`, `xingbu`, `libu`, `hubu`, `gongbu`, `libu_hr`: ministry execution.

Agents must not call an external state CLI. They should follow the skill workflow and return role-scoped outputs.

## Context Control

Do not paste the entire skill into every agent. Prefer short agent prompts that say:

- Use the canonical `sansheng-liubu` skill.
- Stay within this role's boundary.
- Return the role-specific output contract.
