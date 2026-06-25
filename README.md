# Agent-Team

一个面向 Codex / Claude Code 的“三省六部制”多 agent 协作系统。

本项目基于 [cft0808/edict](https://github.com/cft0808/edict) 的制度化多 agent 思路重新收束为轻量仓库：不依赖 Web 服务或数据库，先提供可审计的任务状态机、角色章程、Claude Code subagents、Codex 工作法和 Python CLI。目标是让复杂任务可以被拆解、审议、派发、并行执行，并最终综合输出结果。

## 核心结构

```text
皇上/用户
  -> 太子       分拣输入，创建任务
  -> 中书省     起草方案，拆解任务
  -> 门下省     强制审议，准奏或封驳
  -> 尚书省     派发六部，汇总结果
  -> 六部       并行执行
  -> 尚书省     综合回奏
```

六部职责：

- **兵部**：工程实现、架构、代码、自动化脚本。
- **刑部**：测试、审查、质量、合规、安全边界。
- **礼部**：README、文档、输出格式、体验表达。
- **户部**：数据、统计、成本、资源和指标。
- **工部**：环境、部署、CI/CD、监控、性能和回滚。
- **吏部**：agent 管理、prompt、角色边界、培训和评估。

## 快速开始

```bash
python scripts/sansheng.py init
python scripts/sansheng.py doctor
python scripts/sansheng.py agents
```

创建一个正式任务：

```bash
python scripts/sansheng.py create "搭建三省六部协作骨架" --request "为 Codex 和 Claude Code 建立多 agent 分工系统"
```

记录中书省方案：

```bash
python scripts/sansheng.py plan JJC-YYYYMMDD-001 "建立角色、状态机、CLI 和文档" \
  --step "定义三省六部角色边界" \
  --step "实现任务状态机和审计日志" \
  --step "配置 Claude Code subagents 和 Codex 指令" \
  --acceptance "doctor 检查通过" \
  --acceptance "README 能指导新用户完成一轮任务" \
  --dispatch "兵部: 实现 CLI" \
  --dispatch "刑部: 验证状态机和测试"
```

提交门下省审议并准奏：

```bash
python scripts/sansheng.py state JJC-YYYYMMDD-001 Menxia "方案提交门下省审议" --actor zhongshu
python scripts/sansheng.py review JJC-YYYYMMDD-001 approve "四项审议通过" --actor menxia
python scripts/sansheng.py state JJC-YYYYMMDD-001 Assigned "门下准奏，转尚书省派发" --actor zhongshu
```

派发六部、记录产出、生成回奏：

```bash
python scripts/sansheng.py dispatch JJC-YYYYMMDD-001 bingbu "实现核心 CLI" --detail "任务创建、流转、派发、报告"
python scripts/sansheng.py state JJC-YYYYMMDD-001 Doing "六部开始执行" --actor shangshu
python scripts/sansheng.py todo JJC-YYYYMMDD-001 B1 "核心 CLI 实现" completed --owner bingbu --detail "已完成 sansheng.py"
python scripts/sansheng.py done JJC-YYYYMMDD-001 "系统骨架已完成" "完成三省六部协作骨架" --actor shangshu
python scripts/sansheng.py report JJC-YYYYMMDD-001
```

## 给 Codex 使用

Codex 会读取根目录的 [AGENTS.md](AGENTS.md)。在本仓库内处理正式任务时，按其中流程工作：

- 有 subagent 能力时，按角色分派。
- 没有 subagent 能力时，按“角色 pass”顺序执行，并记录每一步。
- 所有正式任务使用 `scripts/sansheng.py` 留痕。

## 给 Claude Code 使用

Claude Code subagents 已放在 [.claude/agents](.claude/agents)：

- `taizi`
- `zhongshu`
- `menxia`
- `shangshu`
- `bingbu`
- `xingbu`
- `libu`
- `hubu`
- `gongbu`
- `libu_hr`

在 Claude Code 中可以按任务阶段调用相应 subagent。完整说明见 [docs/codex-claude-code.md](docs/codex-claude-code.md)。

## 仓库目录

```text
AGENTS.md                 Codex 根级工作法
.claude/agents/           Claude Code subagent 定义
.codex/prompts/           Codex 可复制 prompt
agents/                   角色章程
config/                   状态机和角色配置
scripts/sansheng.py       任务账本 CLI
docs/                     架构、手册、输出契约
schemas/task.schema.json  任务数据结构
tests/                    CLI 回归测试
examples/                 示例任务
```

## 验证

```bash
python scripts/sansheng.py doctor
python -m unittest discover -s tests
```

## 设计取舍

- 保留 `edict` 的制度化分权：规划、审议、派发、执行、回奏互相分离。
- 不引入数据库、Web UI 或长期运行服务，降低在 Codex/Claude Code 中使用的门槛。
- 将看板变成 JSON/JSONL 任务账本，方便后续接入 Web UI、GitHub Issues、Notion 或 CI。
- 所有 agent prompt 都是普通 Markdown，便于版本化审查。

