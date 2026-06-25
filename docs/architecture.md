# Skill Architecture

Agent-Team is now a skill-first system. The canonical workflow is stored in `skills/sansheng-liubu/`, and host-specific adapters stay thin.

```mermaid
flowchart TD
    U["User request"] --> S["$sansheng-liubu skill"]
    S --> T["太子: intake"]
    T --> Z["中书省: plan"]
    Z --> M["门下省: review"]
    M -->|封驳| Z
    M -->|准奏| SH["尚书省: dispatch"]
    SH --> B["兵部"]
    SH --> X["刑部"]
    SH --> L["礼部"]
    SH --> H["户部"]
    SH --> G["工部"]
    SH --> R["吏部"]
    B --> SH
    X --> SH
    L --> SH
    H --> SH
    G --> SH
    R --> SH
    SH --> Q["刑部/门下复核"]
    Q -->|repair <= 2 rounds| SH
    Q --> O["最终回奏"]
```

## Single Source of Truth

- `skills/sansheng-liubu/SKILL.md`: trigger metadata and core workflow.
- `skills/sansheng-liubu/references/`: detailed contracts loaded only when needed.
- `.claude/commands/sansheng.md`: alias that invokes the skill.
- `.claude/agents/*.md`: role adapters that stay within one office or ministry.

## Non-Goals

- No required service.
- No required database.
- No required Python control plane.
- No hidden infinite review loop.

