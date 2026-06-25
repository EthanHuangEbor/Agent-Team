# Sample Invocation

Codex:

```text
Use $sansheng-liubu to create a release checklist for this repository, dispatch the relevant ministries, run self-review twice at most, and return the final memorial.
```

Claude Code:

```text
/sansheng 为这个仓库生成发布前检查清单，并用门下省和刑部自审查
```

Expected result shape:

- 太子: title, goal, constraints, expected output.
- 中书省: plan, acceptance criteria, ministry routing.
- 门下省: approval or rejection across feasibility, completeness, risk, resources.
- 尚书省: dispatch table.
- 六部: concrete results or explicit non-applicability.
- 自迭代: at most two repair rounds.
- 回奏: final evidence-backed synthesis.

