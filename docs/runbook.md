# Runbook

## 1. Start a Task

```bash
python scripts/sansheng.py init
python scripts/sansheng.py create "一句中文标题" --request "用户原始需求"
```

The command prints a task id such as `JJC-20260625-001`.

## 2. Zhongshu Drafts a Plan

```bash
python scripts/sansheng.py plan JJC-20260625-001 "方案摘要" \
  --step "步骤一" \
  --step "步骤二" \
  --acceptance "验收标准一" \
  --dispatch "兵部: 工程实现" \
  --actor zhongshu

python scripts/sansheng.py state JJC-20260625-001 Menxia "方案提交门下省审议" --actor zhongshu
python scripts/sansheng.py flow JJC-20260625-001 "中书省" "门下省" "提交方案审议" --actor zhongshu
```

## 3. Menxia Reviews

Approve:

```bash
python scripts/sansheng.py review JJC-20260625-001 approve "四项审议通过" \
  --feasibility "依赖明确" \
  --completeness "覆盖目标和验收" \
  --risk "风险可控" \
  --resources "派发合理" \
  --actor menxia

python scripts/sansheng.py state JJC-20260625-001 Assigned "门下准奏，转尚书省派发" --actor menxia
```

Reject:

```bash
python scripts/sansheng.py review JJC-20260625-001 reject "缺少验收标准和回滚方案" --actor menxia
python scripts/sansheng.py state JJC-20260625-001 Zhongshu "门下封驳，退回补充" --actor menxia
```

## 4. Shangshu Dispatches

```bash
python scripts/sansheng.py dispatch JJC-20260625-001 bingbu "实现核心逻辑" --detail "CLI 与状态机"
python scripts/sansheng.py dispatch JJC-20260625-001 xingbu "验证状态机" --detail "doctor 与单元测试"
python scripts/sansheng.py state JJC-20260625-001 Doing "六部开始执行" --actor shangshu
```

## 5. Ministries Report

```bash
python scripts/sansheng.py progress JJC-20260625-001 "兵部正在实现 CLI" "设计✅|编码🔄|测试" --actor bingbu
python scripts/sansheng.py todo JJC-20260625-001 B1 "CLI 实现" completed --owner bingbu --detail "create/state/dispatch/report 已完成"
python scripts/sansheng.py todo JJC-20260625-001 X1 "状态机验证" completed --owner xingbu --detail "doctor 和 unittest 通过"
```

## 6. Final Memorial

```bash
python scripts/sansheng.py done JJC-20260625-001 "最终产物摘要" "完成并验证" --actor shangshu
python scripts/sansheng.py report JJC-20260625-001 --out data/reports/JJC-20260625-001.md
```

## Recovery

Use `--force` only for manual recovery from a corrupted or imported task state:

```bash
python scripts/sansheng.py state JJC-20260625-001 Doing "人工恢复" --force --actor shangshu
```

Run `doctor` after recovery.

