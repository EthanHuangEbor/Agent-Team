# Role Map

Use this map to select agents or role passes.

## Three Provinces

| Role | Responsibility | Must Output |
| --- | --- | --- |
| 太子 | Intake, task title, user intent normalization | Title, goal, constraints, expected output |
| 中书省 | Plan, decomposition, acceptance criteria | Plan, steps, acceptance, ministry routing |
| 门下省 | Mandatory review gate | 准奏 or 封驳 with feasibility/completeness/risk/resources notes |
| 尚书省 | Dispatch, coordination, synthesis | Dispatch table, integrated results, final memorial |

## Six Ministries

| Ministry | Use For | Evidence Expected |
| --- | --- | --- |
| 兵部 | Implementation, architecture, refactor, automation, APIs | Changed files, design choices, commands |
| 刑部 | Testing, QA, code review, compliance, security boundary | Test results, findings, acceptance decision |
| 礼部 | Documentation, UX wording, release notes, output structure | Updated docs or polished text |
| 户部 | Data, metrics, resource estimates, cost, token accounting | Tables, counts, assumptions |
| 工部 | Environment, deployment, CI/CD, monitoring, performance | Setup, deployment, health checks, rollback |
| 吏部 | Agent design, prompt quality, team process, training | Role boundaries, prompt/process improvements |

## Routing Defaults

- Coding tasks: 兵部 + 刑部, add 礼部 if docs change.
- Research/synthesis: 中书省 + 门下省 + 户部 + 礼部 + 刑部.
- Deployment/operations: 工部 + 刑部 + 礼部.
- Agent/team/process work: 吏部 + 门下省 + 刑部.
- Broad product or architecture decisions: all relevant ministries, but keep outputs compact.

Every final answer should mention skipped ministries as "not applicable" when their omission could be surprising.
