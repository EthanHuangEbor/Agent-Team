# Example Task

```bash
python scripts/sansheng.py init
python scripts/sansheng.py create "生成项目发布检查清单" --request "请为这个仓库生成发布前检查清单"
python scripts/sansheng.py plan JJC-20260625-001 "生成发布前检查清单并验证命令可用" --step "梳理仓库结构" --step "编写检查清单" --acceptance "doctor 通过" --dispatch "礼部: 文档" --dispatch "刑部: 验证"
python scripts/sansheng.py state JJC-20260625-001 Menxia "提交审议" --actor zhongshu
python scripts/sansheng.py review JJC-20260625-001 approve "范围清晰，验收明确" --actor menxia
python scripts/sansheng.py state JJC-20260625-001 Assigned "准奏，交尚书省派发" --actor menxia
python scripts/sansheng.py dispatch JJC-20260625-001 libu "编写发布检查清单" --detail "覆盖安装、测试、文档、提交"
python scripts/sansheng.py dispatch JJC-20260625-001 xingbu "验证检查清单" --detail "确认命令存在且顺序合理"
python scripts/sansheng.py state JJC-20260625-001 Doing "开始执行" --actor shangshu
python scripts/sansheng.py todo JJC-20260625-001 L1 "发布检查清单" completed --owner libu --detail "已写入 docs/release-checklist.md"
python scripts/sansheng.py todo JJC-20260625-001 X1 "命令验证" completed --owner xingbu --detail "doctor 和 unittest 通过"
python scripts/sansheng.py done JJC-20260625-001 "发布检查清单已完成" "完成文档并通过验证" --actor shangshu
python scripts/sansheng.py report JJC-20260625-001
```

