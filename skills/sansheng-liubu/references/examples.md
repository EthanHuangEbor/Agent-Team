# Examples

## Formal Task Success

User: "Use 三省六部 to create a release checklist for this repo."

Expected shape:

- 太子: title and goal.
- 中书省: plan with acceptance criteria.
- 门下省: approves because scope, risk, and resources are clear.
- 尚书省: dispatches 礼部 for docs, 刑部 for validation, 工部 if CI/deployment is relevant.
- 六部: each returns concrete results or "not applicable".
- 回奏: includes checklist path or checklist content, validation evidence, and remaining risks.

## Menxia Rejection

Bad Zhongshu plan: "Write some docs and finish."

门下省 must reject:

- Feasibility: unclear.
- Completeness: missing target docs and acceptance criteria.
- Risk: no validation or rollback.
- Resources: ministries not assigned.

Zhongshu must revise before Shangshu can dispatch.

## Two-Round Stop

If Xingbu rejects output twice because tests cannot run or evidence is missing, stop after the second repair attempt and report the unresolved risk. Do not continue with a third repair loop.
