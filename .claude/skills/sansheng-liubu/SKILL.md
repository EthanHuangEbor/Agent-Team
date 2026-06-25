---
name: sansheng-liubu
description: "Use this skill for complex Codex or Claude Code work that benefits from 三省六部 multi-agent governance: task triage and decomposition, Zhongshu planning, Menxia feasibility/completeness/risk/resource review, Shangshu dispatch to ministries, parallel or role-pass execution, Xingbu quality review, two-round self-iteration, and final synthesized memorial output. Trigger when the user asks for multi-agent teamwork, task breakdown, self-review, self-iteration, coordinated implementation, research synthesis, architecture review, or 三省六部 handling."
---

# 三省六部 Skill

Use this skill as the primary entrypoint. Do not require an external state CLI or runtime before doing the work.

## Core Workflow

1. **太子**: classify the request. For formal work, restate the title, goal, constraints, and expected output.
2. **中书省**: draft the plan, decomposition, acceptance criteria, and ministry routing.
3. **门下省**: review the plan across feasibility, completeness, risk, and resources. Reject incomplete plans and require a corrected Zhongshu plan.
4. **尚书省**: dispatch approved work to the relevant ministries.
5. **六部**: execute or analyze by role. Use real subagents when available; otherwise run explicit role passes.
6. **刑部 + 门下复核**: review execution quality. Iterate at most two rounds.
7. **回奏**: synthesize results, evidence, validation, remaining risks, and next steps.

Read `references/workflow-contract.md` before handling any formal task. Read `references/role-map.md` when choosing ministries. Read `references/self-iteration.md` before review or repair loops. Read `references/output-contract.md` before final output. Read `references/claude-code-adapter.md` when invoked from Claude Code or when maintaining `.claude/` adapters.

## Delegation Rule

If the host exposes real subagent or multi-agent tools, delegate concrete, non-overlapping tasks to the relevant roles and integrate their results. If no such tool exists, simulate the same offices as labeled role passes in one response. In both cases, preserve the governance order: no Shangshu dispatch before Menxia approval.

## Two-Round Iteration Limit

Run at most two repair rounds after execution begins:

- Round 1: Xingbu or Menxia identifies issues; Zhongshu/Shangshu revises and ministries repair.
- Round 2: repeat only for unresolved blocking issues.
- If still not accepted after round 2, stop and report the unmet criteria, risk, and recommended human decision. Do not continue polishing indefinitely.

## Required Final Shape

Final answers must include:

- The task title and goal.
- Zhongshu plan and Menxia decision.
- Shangshu dispatch summary.
- Ministry contributions, including "not applicable" where a ministry was intentionally skipped.
- Validation evidence: commands, files, citations, screenshots, or reasoning checks actually used.
- Remaining risks or open items.

Use concise section labels. Do not claim that agents executed work unless there is either a real subagent result or an explicit role-pass result.
