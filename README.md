# Agent-Team

Agent-Team 是一个面向 **Codex / Claude Code** 的三省六部制 multi-agent skill。它把复杂任务变成一套可调用、可审议、可自迭代的协作流程：用户只需要调用 `$sansheng-liubu` 或 Claude Code 的 `/sansheng`，系统就会按“太子分拣、中书拟案、门下审议、尚书派发、六部执行、刑部复核、最终回奏”的制度完成任务。

## 灵感来源

本项目的制度灵感来自 [cft0808/edict](https://github.com/cft0808/edict)。`edict` 用中国古代“三省六部”的权责结构来重新设计 AI 多 agent 协作：不是让几个 agent 随便聊天，而是让规划、审议、派发、执行、复核分权制衡。

Agent-Team 继承的是这套制度思想：

- **中书省负责规划**，避免执行者一上来就动手。
- **门下省负责封驳**，让方案先过可行性、完整性、风险、资源四项审查。
- **尚书省负责派发**，只在准奏后调度六部。
- **六部各司其职**，让工程、测试、文档、数据、部署、agent 管理都有明确责任。
- **刑部和门下复核**，让结果在交付前自审查、自修正。

但 Agent-Team 的实现方式不同：它不是 Web 服务、数据库或 Python 任务账本，而是一个 **skill-first** 包，可以被 Codex 和 Claude Code 原生调用。

## 具体如何实现

核心入口是 [`skills/sansheng-liubu/SKILL.md`](skills/sansheng-liubu/SKILL.md)。这个文件定义了触发条件、主流程、真实 subagent 优先规则、两轮自迭代上限和最终输出要求。

配套实现分为三层：

1. **Canonical Skill**
   - [`skills/sansheng-liubu/SKILL.md`](skills/sansheng-liubu/SKILL.md)：唯一权威入口。
   - [`skills/sansheng-liubu/agents/openai.yaml`](skills/sansheng-liubu/agents/openai.yaml)：Codex UI 元数据和默认调用 prompt。
   - [`skills/sansheng-liubu/references`](skills/sansheng-liubu/references)：流程契约、角色映射、自迭代规则、输出契约、Claude Code 适配说明。

2. **Claude Code 适配层**
   - [`.claude/skills/sansheng-liubu`](.claude/skills/sansheng-liubu)：项目内 Claude skill 副本。
   - [`.claude/commands/sansheng.md`](.claude/commands/sansheng.md)：`/sansheng` 薄命令，只负责调用 skill。
   - [`.claude/agents`](.claude/agents)：太子、中书省、门下省、尚书省、六部的角色适配器。

3. **同步与验收**
   - [`scripts/sync-sansheng-skill.ps1`](scripts/sync-sansheng-skill.ps1)：把 canonical skill 同步到本机 Codex / Claude Code skill 目录。
   - [`tests/skill-static-check.ps1`](tests/skill-static-check.ps1)：检查 skill、Claude command、agents、旧 CLI 残留和输出契约。

工作时，如果宿主环境有真实 subagent / multi-agent 工具，skill 会要求按职责派发给对应 agent；如果没有真实 subagent，就用明确标注的角色 pass 模拟同一套制度。无论哪种方式，都必须先经过门下省审议，尚书省才能派发。

## 下载和安装 Skill

### 方式一：克隆仓库后同步到本机

```powershell
git clone git@github.com:EthanHuangEbor/Agent-Team.git
cd Agent-Team
.\scripts\sync-sansheng-skill.ps1 -DryRun
.\scripts\sync-sansheng-skill.ps1 -Force
```

同步目标：

- Codex：`%USERPROFILE%\.codex\skills\sansheng-liubu`
- Claude Code：`%USERPROFILE%\.claude\skills\omc-learned\sansheng-liubu`
- 当前仓库 Claude 项目 skill：`.claude\skills\sansheng-liubu`

如果设置了 `CODEX_HOME`，Codex 目标会改为：

```text
$CODEX_HOME\skills\sansheng-liubu
```

### 方式二：只复制 skill 包

如果你不想同步整个仓库，只需要复制这个目录：

```text
skills/sansheng-liubu
```

放到 Codex：

```text
%USERPROFILE%\.codex\skills\sansheng-liubu
```

或放到 Claude Code：

```text
%USERPROFILE%\.claude\skills\omc-learned\sansheng-liubu
```

然后重启 Codex / Claude Code，让工具重新扫描 skills。

## 如何调用

Codex：

```text
Use $sansheng-liubu to decompose this goal, dispatch the ministries, self-review twice at most, and return the final memorial.
```

Claude Code：

```text
/sansheng 为这个仓库建立发布检查清单，并自审查两轮封顶
```

也可以直接在自然语言里说：

```text
请用三省六部制处理这个任务：设计一个多 agent 代码审查流程。
```

## 能达到什么效果

调用 `sansheng-liubu` 后，复杂任务会被组织成下面的产出链路：

1. **太子 brief**
   - 判断是否需要完整三省六部流程。
   - 提炼任务标题、目标、约束和预期交付物。

2. **中书省方案**
   - 拆解任务。
   - 给出执行步骤、验收标准和六部派发建议。

3. **门下省审议**
   - 从可行性、完整性、风险、资源四个维度审查。
   - 方案不完整时会“封驳”，要求中书省补案。

4. **尚书省派发**
   - 只在门下省准奏后派发。
   - 根据任务类型选择兵部、刑部、礼部、户部、工部、吏部。

5. **六部执行**
   - **兵部**：工程实现、架构、代码、自动化。
   - **刑部**：测试、质量、合规、安全边界。
   - **礼部**：文档、README、发布说明、沟通表达。
   - **户部**：数据、统计、成本、资源和指标。
   - **工部**：环境、部署、CI/CD、监控、回滚。
   - **吏部**：agent 设计、prompt、流程、培训和评估。

6. **自审查与自迭代**
   - 门下省和刑部可以要求返工。
   - 最多两轮修正，避免无限循环。
   - 第二轮仍不通过时，停止并回奏风险，而不是假装完成。

7. **最终回奏**
   - 汇总实际产物、各部贡献、验证结果、未完成事项和风险。
   - 不用角色名冒充成果，每个角色都必须给出证据或明确说明不适用。

## 验证

```powershell
powershell -ExecutionPolicy Bypass -File .\tests\skill-static-check.ps1
$env:PYTHONUTF8='1'; python C:\Users\Lenovo\.codex\skills\.system\skill-creator\scripts\quick_validate.py .\skills\sansheng-liubu
```

静态验收会检查：

- canonical skill 是否存在；
- `openai.yaml` 是否指向 `$sansheng-liubu`；
- Claude `/sansheng` 命令是否存在且保持薄入口；
- Claude agents 是否仍引用旧状态 CLI；
- 主文档是否仍推荐旧流程。

## Repository Layout

```text
skills/sansheng-liubu/          Canonical Codex / Claude skill package
  SKILL.md                      Trigger metadata and core workflow
  agents/openai.yaml            Codex UI metadata
  references/                   Workflow, role map, iteration, output contracts

.claude/skills/sansheng-liubu/  Claude project skill adapter
.claude/commands/sansheng.md    Claude slash command alias
.claude/agents/                 Claude role adapters
docs/                           Architecture and install/sync docs
scripts/sync-sansheng-skill.ps1 Idempotent local sync helper
tests/skill-static-check.ps1    Static acceptance checks
```

## Design Notes

- Inspired by [cft0808/edict](https://github.com/cft0808/edict), but packaged as a portable skill.
- Skill 是唯一权威来源，Claude command 和 agents 只是适配层。
- 不依赖 Python 任务账本、数据库或后台服务。
- 默认两轮自迭代封顶，既能自修正，又不会陷入无限返工。
