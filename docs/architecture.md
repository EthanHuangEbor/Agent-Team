# Architecture

Agent-Team 是一个轻量控制平面。它不强行替代 Codex 或 Claude Code 的执行环境，而是为它们提供一套稳定的任务制度、角色边界和审计账本。

## Components

```mermaid
flowchart TD
    U["用户 / 皇上"] --> T["太子: 分拣"]
    T --> Z["中书省: 拟案"]
    Z --> M["门下省: 审议"]
    M -->|准奏| S["尚书省: 派发"]
    M -->|封驳| Z
    S --> B["兵部: 工程"]
    S --> X["刑部: 质量"]
    S --> L["礼部: 文档"]
    S --> H["户部: 数据"]
    S --> G["工部: 部署"]
    S --> R["吏部: Agent"]
    B --> S
    X --> S
    L --> S
    H --> S
    G --> S
    R --> S
    S --> O["最终回奏"]
```

## Layers

- **Role layer**: `agents/` and `.claude/agents/` define responsibilities.
- **Control layer**: `config/state-machine.json` and `config/court.json` define legal movement and routing.
- **Ledger layer**: `scripts/sansheng.py` records tasks in `data/tasks.json` and append-only events in `data/events.jsonl`.
- **Output layer**: `report` renders a final memorial that can be pasted into Codex, Claude Code, GitHub, Notion, or release notes.

## State Machine

```mermaid
stateDiagram-v2
    [*] --> Zhongshu
    Zhongshu --> Menxia
    Menxia --> Zhongshu: reject
    Menxia --> Assigned: approve
    Assigned --> Doing
    Doing --> Review
    Review --> Menxia: recheck
    Review --> Done
    Doing --> Done
    Zhongshu --> Blocked
    Menxia --> Blocked
    Assigned --> Blocked
    Doing --> Blocked
    Review --> Blocked
    Blocked --> Zhongshu
    Blocked --> Assigned
    Blocked --> Doing
    Assigned --> Paused
    Doing --> Paused
    Paused --> Assigned
    Paused --> Doing
    Zhongshu --> Cancelled
    Menxia --> Cancelled
    Assigned --> Cancelled
    Doing --> Cancelled
    Review --> Cancelled
```

## Event Shape

Every CLI command appends JSONL:

```json
{
  "event_id": "uuid",
  "at": "2026-06-25T07:00:00Z",
  "type": "task.dispatch",
  "task_id": "JJC-20260625-001",
  "actor": "shangshu",
  "payload": {
    "department": "bingbu",
    "title": "实现核心 CLI"
  }
}
```

This makes the system replayable without a service dependency.

## Extension Points

- Replace `data/tasks.json` with SQLite or Postgres.
- Mirror task states to GitHub Issues.
- Render JSONL events into a web Kanban board.
- Add real parallel subagent execution where the host supports it.
- Add model-specific prompt packs under `.codex/prompts` or `.claude/agents`.

