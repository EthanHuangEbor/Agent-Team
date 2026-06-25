#!/usr/bin/env python3
"""Lightweight task ledger for the Codex / Claude Code 三省六部制 workflow."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.environ.get("SANSHENG_DATA_DIR", REPO_ROOT / "data"))
TASKS_PATH = DATA_DIR / "tasks.json"
EVENTS_PATH = DATA_DIR / "events.jsonl"
COURT_PATH = REPO_ROOT / "config" / "court.json"
STATE_MACHINE_PATH = REPO_ROOT / "config" / "state-machine.json"


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def die(message: str, code: int = 1) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(code)


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"{path} is not valid JSON: {exc}")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def append_event(event: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    event.setdefault("event_id", str(uuid.uuid4()))
    event.setdefault("at", now_utc())
    with EVENTS_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def load_tasks() -> dict[str, Any]:
    return read_json(TASKS_PATH, {"version": 1, "tasks": []})


def save_tasks(data: dict[str, Any]) -> None:
    write_json(TASKS_PATH, data)


def load_court() -> dict[str, Any]:
    return read_json(COURT_PATH, {})


def load_machine() -> dict[str, Any]:
    return read_json(STATE_MACHINE_PATH, {})


def task_by_id(data: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in data.get("tasks", []):
        if task.get("id") == task_id:
            return task
    die(f"task not found: {task_id}")


def agent_ids() -> set[str]:
    return {agent["id"] for agent in load_court().get("agents", [])}


def agent_name_map() -> dict[str, str]:
    return {agent["id"]: agent["name"] for agent in load_court().get("agents", [])}


def state_names() -> set[str]:
    return set(load_machine().get("states", []))


def can_transition(current: str, target: str) -> bool:
    machine = load_machine()
    if current == target:
        return True
    return target in machine.get("transitions", {}).get(current, [])


def ensure_state(target: str) -> None:
    states = state_names()
    if target not in states:
        die(f"unknown state {target}; expected one of: {', '.join(sorted(states))}")


def generate_task_id(data: dict[str, Any]) -> str:
    prefix = load_court().get("task_id_prefix", "JJC")
    today = dt.datetime.now().strftime("%Y%m%d")
    stem = f"{prefix}-{today}-"
    max_seen = 0
    for task in data.get("tasks", []):
        task_id = task.get("id", "")
        if task_id.startswith(stem):
            try:
                max_seen = max(max_seen, int(task_id.rsplit("-", 1)[1]))
            except ValueError:
                continue
    return f"{stem}{max_seen + 1:03d}"


def add_flow(task: dict[str, Any], from_agent: str, to_agent: str, remark: str, actor: str) -> dict[str, Any]:
    item = {
        "at": now_utc(),
        "from": from_agent,
        "to": to_agent,
        "remark": remark,
        "actor": actor,
    }
    task.setdefault("flow", []).append(item)
    task["updated_at"] = item["at"]
    return item


def cmd_init(_args: argparse.Namespace) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_PATH.exists():
        save_tasks({"version": 1, "tasks": []})
    if not EVENTS_PATH.exists():
        EVENTS_PATH.write_text("", encoding="utf-8")
    print(f"initialized ledger at {DATA_DIR}")


def cmd_create(args: argparse.Namespace) -> None:
    data = load_tasks()
    task_id = args.id or generate_task_id(data)
    if any(task.get("id") == task_id for task in data.get("tasks", [])):
        die(f"task already exists: {task_id}")
    initial = load_machine().get("initial", "Zhongshu")
    ensure_state(initial)
    timestamp = now_utc()
    task = {
        "id": task_id,
        "title": args.title,
        "state": initial,
        "source": args.source,
        "original_request": args.request or "",
        "created_at": timestamp,
        "updated_at": timestamp,
        "plan": None,
        "review": None,
        "progress": [],
        "todos": [],
        "dispatches": [],
        "outputs": [],
        "flow": [],
    }
    add_flow(task, args.source, initial, args.note or "太子整理旨意，转交中书省", args.actor)
    data.setdefault("tasks", []).append(task)
    save_tasks(data)
    append_event({"type": "task.created", "task_id": task_id, "actor": args.actor, "payload": task})
    print(f"{task_id} created in {initial}: {args.title}")


def cmd_state(args: argparse.Namespace) -> None:
    ensure_state(args.state)
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    current = task["state"]
    if not args.force and not can_transition(current, args.state):
        die(f"illegal transition: {current} -> {args.state}; pass --force only for manual recovery")
    task["state"] = args.state
    task["updated_at"] = now_utc()
    entry = {
        "at": task["updated_at"],
        "state": args.state,
        "note": args.note,
        "actor": args.actor,
    }
    task.setdefault("state_history", []).append(entry)
    save_tasks(data)
    append_event({"type": "task.state", "task_id": args.task_id, "actor": args.actor, "payload": entry})
    print(f"{args.task_id}: {current} -> {args.state}")


def cmd_flow(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    item = add_flow(task, args.from_agent, args.to_agent, args.remark, args.actor)
    save_tasks(data)
    append_event({"type": "task.flow", "task_id": args.task_id, "actor": args.actor, "payload": item})
    print(f"{args.task_id}: {args.from_agent} -> {args.to_agent}")


def cmd_progress(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    item = {
        "at": now_utc(),
        "actor": args.actor,
        "current": args.current,
        "checklist": [part.strip() for part in args.checklist.split("|") if part.strip()],
    }
    task.setdefault("progress", []).append(item)
    task["updated_at"] = item["at"]
    save_tasks(data)
    append_event({"type": "task.progress", "task_id": args.task_id, "actor": args.actor, "payload": item})
    print(f"{args.task_id}: progress recorded")


def cmd_plan(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    plan = {
        "at": now_utc(),
        "actor": args.actor,
        "summary": args.summary,
        "steps": args.step or [],
        "acceptance": args.acceptance or [],
        "dispatch": args.dispatch or [],
    }
    task["plan"] = plan
    task["updated_at"] = plan["at"]
    save_tasks(data)
    append_event({"type": "task.plan", "task_id": args.task_id, "actor": args.actor, "payload": plan})
    print(f"{args.task_id}: plan recorded")


def cmd_review(args: argparse.Namespace) -> None:
    if args.verdict not in {"approve", "reject"}:
        die("review verdict must be approve or reject")
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    review = {
        "at": now_utc(),
        "actor": args.actor,
        "verdict": args.verdict,
        "notes": args.note,
        "dimensions": {
            "feasibility": args.feasibility,
            "completeness": args.completeness,
            "risk": args.risk,
            "resources": args.resources,
        },
    }
    task["review"] = review
    task["updated_at"] = review["at"]
    save_tasks(data)
    append_event({"type": "task.review", "task_id": args.task_id, "actor": args.actor, "payload": review})
    print(f"{args.task_id}: review {args.verdict}")


def cmd_dispatch(args: argparse.Namespace) -> None:
    agents = agent_ids()
    if args.department not in agents:
        die(f"unknown department {args.department}; expected one of: {', '.join(sorted(agents))}")
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    item = {
        "id": f"D-{len(task.get('dispatches', [])) + 1:03d}",
        "at": now_utc(),
        "department": args.department,
        "title": args.title,
        "detail": args.detail or "",
        "status": args.status,
        "actor": args.actor,
    }
    task.setdefault("dispatches", []).append(item)
    task["updated_at"] = item["at"]
    save_tasks(data)
    append_event({"type": "task.dispatch", "task_id": args.task_id, "actor": args.actor, "payload": item})
    print(f"{args.task_id}: dispatched {item['id']} to {args.department}")


def cmd_todo(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    item = {
        "todo_id": args.todo_id,
        "at": now_utc(),
        "owner": args.owner,
        "title": args.title,
        "status": args.status,
        "detail": args.detail or "",
        "actor": args.actor,
    }
    todos = task.setdefault("todos", [])
    for index, todo in enumerate(todos):
        if todo.get("todo_id") == args.todo_id:
            todos[index] = item
            break
    else:
        todos.append(item)
    task["updated_at"] = item["at"]
    save_tasks(data)
    append_event({"type": "task.todo", "task_id": args.task_id, "actor": args.actor, "payload": item})
    print(f"{args.task_id}: todo {args.todo_id} {args.status}")


def cmd_done(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    current = task["state"]
    if not args.force and not can_transition(current, "Done"):
        die(f"illegal transition: {current} -> Done; pass --force only for manual recovery")
    output = {
        "at": now_utc(),
        "actor": args.actor,
        "summary": args.summary,
        "output": args.output,
    }
    task.setdefault("outputs", []).append(output)
    task["state"] = "Done"
    task["updated_at"] = output["at"]
    add_flow(task, args.actor, "皇上", f"✅ 回奏：{args.summary}", args.actor)
    save_tasks(data)
    append_event({"type": "task.done", "task_id": args.task_id, "actor": args.actor, "payload": output})
    print(f"{args.task_id}: Done")


def render_task(task: dict[str, Any]) -> str:
    names = agent_name_map()

    def label(agent_id: str) -> str:
        name = names.get(agent_id)
        return f"{name}({agent_id})" if name else agent_id

    lines = [
        f"# 回奏：{task['title']}",
        "",
        f"- 任务ID: {task['id']}",
        f"- 当前状态: {task['state']}",
        f"- 创建时间: {task['created_at']}",
        f"- 更新时间: {task['updated_at']}",
    ]
    if task.get("original_request"):
        lines += ["", "## 原始旨意", "", task["original_request"]]
    if task.get("plan"):
        plan = task["plan"]
        lines += ["", "## 中书省方案", "", plan.get("summary", "")]
        if plan.get("steps"):
            lines += ["", "### 步骤"]
            lines += [f"- {step}" for step in plan["steps"]]
        if plan.get("acceptance"):
            lines += ["", "### 验收"]
            lines += [f"- {item}" for item in plan["acceptance"]]
    if task.get("review"):
        review = task["review"]
        lines += ["", "## 门下省审议", "", f"- 结论: {review.get('verdict')}", f"- 意见: {review.get('notes')}"]
    if task.get("dispatches"):
        lines += ["", "## 尚书省派发"]
        for item in task["dispatches"]:
            lines.append(f"- {item['id']} {label(item['department'])}: {item['title']} ({item['status']})")
    if task.get("todos"):
        lines += ["", "## 六部执行"]
        for todo in task["todos"]:
            lines.append(f"- {label(todo['owner'])} / {todo['todo_id']} / {todo['status']}: {todo['title']}")
            if todo.get("detail"):
                lines.append(f"  - {todo['detail']}")
    if task.get("progress"):
        latest = task["progress"][-1]
        lines += ["", "## 最新进展", "", latest["current"]]
        if latest.get("checklist"):
            lines += [f"- {item}" for item in latest["checklist"]]
    if task.get("outputs"):
        latest_output = task["outputs"][-1]
        lines += ["", "## 最终回奏", "", latest_output.get("summary", ""), "", latest_output.get("output", "")]
    if task.get("flow"):
        lines += ["", "## 流转记录"]
        for item in task["flow"]:
            lines.append(f"- {item['at']} {item['from']} -> {item['to']}: {item['remark']}")
    return "\n".join(lines).rstrip() + "\n"


def cmd_show(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    if args.json:
        print(json.dumps(task, ensure_ascii=False, indent=2))
        return
    print(render_task(task))


def cmd_report(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    report = render_task(task)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(f"wrote {out}")
    else:
        print(report)


def cmd_list_agents(_args: argparse.Namespace) -> None:
    court = load_court()
    for agent in court.get("agents", []):
        print(f"{agent['id']}\t{agent['name']}\t{agent['tier']}\t{agent['mission']}")


def cmd_next(args: argparse.Namespace) -> None:
    data = load_tasks()
    task = task_by_id(data, args.task_id)
    state = task["state"]
    suggestions = {
        "Zhongshu": "中书省起草 plan，然后 state 到 Menxia 并记录 flow。",
        "Menxia": "门下省执行 review；approve 后 state 到 Assigned，reject 后退回 Zhongshu。",
        "Assigned": "尚书省 dispatch 给六部，并 state 到 Doing。",
        "Doing": "六部执行 todo/progress；完成后进入 Review 或 Done。",
        "Review": "刑部或门下省做最终验收；通过后 done，未通过退回 Menxia。",
        "Blocked": "补齐阻塞信息，恢复到 Zhongshu/Assigned/Doing 或 Cancelled。",
        "Paused": "恢复到 Assigned/Doing，或 Cancelled。",
        "Done": "任务已完结，可用 report 导出回奏。",
        "Cancelled": "任务已取消。",
    }
    print(suggestions.get(state, "未知状态，请运行 doctor 检查配置。"))


def cmd_doctor(_args: argparse.Namespace) -> None:
    errors: list[str] = []
    court = load_court()
    machine = load_machine()
    if not court.get("agents"):
        errors.append("config/court.json has no agents")
    states = set(machine.get("states", []))
    if machine.get("initial") not in states:
        errors.append("state-machine initial state is invalid")
    for source, targets in machine.get("transitions", {}).items():
        if source not in states:
            errors.append(f"transition source is not declared: {source}")
        for target in targets:
            if target not in states:
                errors.append(f"transition target is not declared: {source} -> {target}")
    for agent in court.get("agents", []):
        agent_id = agent["id"]
        if not (REPO_ROOT / "agents" / f"{agent_id}.md").exists() and not (
            REPO_ROOT / "agents" / "liubu" / f"{agent_id}.md"
        ).exists():
            errors.append(f"missing agent prompt: {agent_id}")
        if not (REPO_ROOT / ".claude" / "agents" / f"{agent_id}.md").exists():
            errors.append(f"missing Claude agent: {agent_id}")
    data = load_tasks()
    for task in data.get("tasks", []):
        if task.get("state") not in states:
            errors.append(f"{task.get('id')} has invalid state {task.get('state')}")
    if EVENTS_PATH.exists():
        for line_no, line in enumerate(EVENTS_PATH.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"events.jsonl:{line_no} invalid JSON: {exc}")
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        raise SystemExit(1)
    print("doctor ok")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Codex / Claude Code 三省六部制 task ledger")
    parser.set_defaults(func=lambda _args: parser.print_help())
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("init", help="initialize data ledger")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("create", help="create a formal task")
    p.add_argument("title")
    p.add_argument("--request", default="")
    p.add_argument("--source", default="皇上")
    p.add_argument("--note", default="")
    p.add_argument("--id", default="")
    p.add_argument("--actor", default="taizi")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("state", help="change task state")
    p.add_argument("task_id")
    p.add_argument("state")
    p.add_argument("note")
    p.add_argument("--actor", default="system")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_state)

    p = sub.add_parser("flow", help="append a flow record")
    p.add_argument("task_id")
    p.add_argument("from_agent")
    p.add_argument("to_agent")
    p.add_argument("remark")
    p.add_argument("--actor", default="system")
    p.set_defaults(func=cmd_flow)

    p = sub.add_parser("progress", help="record progress")
    p.add_argument("task_id")
    p.add_argument("current")
    p.add_argument("checklist")
    p.add_argument("--actor", default="system")
    p.set_defaults(func=cmd_progress)

    p = sub.add_parser("plan", help="record Zhongshu plan")
    p.add_argument("task_id")
    p.add_argument("summary")
    p.add_argument("--step", action="append")
    p.add_argument("--acceptance", action="append")
    p.add_argument("--dispatch", action="append")
    p.add_argument("--actor", default="zhongshu")
    p.set_defaults(func=cmd_plan)

    p = sub.add_parser("review", help="record Menxia review")
    p.add_argument("task_id")
    p.add_argument("verdict", choices=["approve", "reject"])
    p.add_argument("note")
    p.add_argument("--feasibility", default="")
    p.add_argument("--completeness", default="")
    p.add_argument("--risk", default="")
    p.add_argument("--resources", default="")
    p.add_argument("--actor", default="menxia")
    p.set_defaults(func=cmd_review)

    p = sub.add_parser("dispatch", help="dispatch work to a ministry")
    p.add_argument("task_id")
    p.add_argument("department")
    p.add_argument("title")
    p.add_argument("--detail", default="")
    p.add_argument("--status", default="open")
    p.add_argument("--actor", default="shangshu")
    p.set_defaults(func=cmd_dispatch)

    p = sub.add_parser("todo", help="record or update a ministry todo")
    p.add_argument("task_id")
    p.add_argument("todo_id")
    p.add_argument("title")
    p.add_argument("status")
    p.add_argument("--owner", default="unknown")
    p.add_argument("--detail", default="")
    p.add_argument("--actor", default="system")
    p.set_defaults(func=cmd_todo)

    p = sub.add_parser("done", help="close a task and record final output")
    p.add_argument("task_id")
    p.add_argument("output")
    p.add_argument("summary")
    p.add_argument("--actor", default="shangshu")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("show", help="show a task")
    p.add_argument("task_id")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("report", help="render final memorial report")
    p.add_argument("task_id")
    p.add_argument("--out", default="")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("agents", help="list court agents")
    p.set_defaults(func=cmd_list_agents)

    p = sub.add_parser("next", help="suggest next workflow action")
    p.add_argument("task_id")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("doctor", help="validate config, prompts, tasks, and event log")
    p.set_defaults(func=cmd_doctor)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
