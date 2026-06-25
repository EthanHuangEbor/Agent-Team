# Codex 三省六部制工作法

本仓库采用“三省六部制”处理正式任务。灵感来自
[cft0808/edict](https://github.com/cft0808/edict)，但这里的实现目标是让
Codex / Claude Code 都能直接使用：任务先拆解，再审议，再分工并行，最后综合回奏。

## 什么时候启用

遇到明确交付型任务时启用本流程，例如：实现功能、写报告、做调研、重构、部署、审查、
生成方案。极小的问答或简单命令可以直接处理。

## 强制流程

1. **太子**：分拣输入，提炼一句中文标题，创建任务。
2. **中书省**：起草方案，列出步骤、验收标准、建议派发部门。
3. **门下省**：从可行性、完整性、风险、资源四项审议。明显缺口必须封驳。
4. **尚书省**：按准奏方案派发给六部，收集各部产出。
5. **六部**：按职责执行。兵部做工程实现，刑部做测试审查，礼部做文档体验，户部做数据成本，工部做部署运维，吏部做 agent/流程管理。
6. **回奏**：综合执行结果、验证情况、风险和后续建议。

## 任务留痕

所有正式任务都使用 `scripts/sansheng.py` 记录：

```bash
python scripts/sansheng.py init
python scripts/sansheng.py create "任务标题" --request "用户原始需求"
python scripts/sansheng.py plan JJC-YYYYMMDD-001 "方案摘要" --step "步骤" --acceptance "验收标准"
python scripts/sansheng.py state JJC-YYYYMMDD-001 Menxia "方案提交门下省审议" --actor zhongshu
python scripts/sansheng.py review JJC-YYYYMMDD-001 approve "准奏" --actor menxia
python scripts/sansheng.py state JJC-YYYYMMDD-001 Assigned "门下准奏，转尚书省派发" --actor zhongshu
python scripts/sansheng.py dispatch JJC-YYYYMMDD-001 bingbu "实现核心逻辑" --detail "范围和产出"
python scripts/sansheng.py todo JJC-YYYYMMDD-001 B1 "核心逻辑实现" completed --owner bingbu --detail "产出摘要"
python scripts/sansheng.py done JJC-YYYYMMDD-001 "最终产出" "摘要" --actor shangshu
```

如运行环境没有真实 subagent 工具，就按角色顺序进行“角色 pass”，并在输出中标明
`中书省方案`、`门下省审议`、`尚书省派发`、`六部执行`、`最终回奏`。

## 输出标准

最终回复必须包含：

- 已完成的实际产物或代码路径。
- 各部门关键贡献。
- 验证结果，包含运行过的命令。
- 未完成事项或风险，如果有。

不要跳过门下省审议；不要在门下省准奏后停止；不要把未经审议的方案直接交给六部。

