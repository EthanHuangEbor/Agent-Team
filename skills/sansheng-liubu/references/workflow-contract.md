# Workflow Contract

The 三省六部 workflow is a governance protocol for complex work. Keep the order strict.

## Formal Task Flow

1. **太子: intake**
   - Decide whether the user request is formal work.
   - Produce a short title, goal, constraints, and expected output.
   - For simple Q&A, answer directly without invoking the full court.

2. **中书省: planning**
   - Draft the execution plan.
   - Define acceptance criteria.
   - Identify relevant ministries.
   - Do not implement during this step.

3. **门下省: review gate**
   - Review feasibility, completeness, risk, and resources.
   - If any required dimension is weak, return **封驳** with concrete fixes.
   - If acceptable, return **准奏** and allow dispatch.

4. **尚书省: dispatch**
   - Assign approved work to ministries.
   - Prefer real subagents when available.
   - Use role passes when subagents are unavailable.
   - Track which ministries were used and why.

5. **六部: execution**
   - Execute only within each ministry's responsibility.
   - Return evidence, changed files, commands, analysis, or explicit non-applicability.

6. **刑部 and 门下: review**
   - Xingbu checks quality, tests, compliance, and gaps.
   - Menxia checks whether the final output still satisfies the approved plan.
   - Trigger at most two repair rounds.

7. **回奏: final synthesis**
   - Report the result in one coherent answer.
   - Include evidence and unresolved risks.

## Hard Stops

- Do not dispatch before Menxia approval.
- Do not let Menxia always approve. Missing acceptance criteria, missing risk handling, or unclear scope must be rejected.
- Do not run more than two repair rounds.
- Do not hide failed or skipped validation.
