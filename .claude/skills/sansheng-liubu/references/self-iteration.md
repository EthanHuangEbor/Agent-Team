# Self-Iteration Contract

The system is self-checking, not endlessly self-rewriting.

## Review Dimensions

Menxia reviews plans:

- Feasibility: can the path be executed with available tools and context?
- Completeness: does the plan cover the user's actual request and acceptance criteria?
- Risk: are failure modes, permissions, data risks, and rollback needs visible?
- Resources: are the right ministries assigned with reasonable scope?

Xingbu reviews execution:

- Correctness and edge cases.
- Tests or evidence.
- Compliance with user constraints.
- Whether final claims are supported by actual work.

## Iteration Limit

Use a maximum of two repair rounds after the first execution attempt.

```text
Execution attempt
  -> Review
  -> Repair round 1 if needed
  -> Review
  -> Repair round 2 if still needed
  -> Final review
  -> Stop with pass or risk report
```

If the second repair round still fails, stop. The final output must say:

- Which criteria remain unmet.
- Why the team could not resolve them.
- What human decision or extra input is needed.

## Anti-Patterns

- "Looks good" review without naming the four Menxia dimensions.
- Infinite refinement loops.
- Replanning after dispatch without explaining why Menxia approval no longer holds.
- Claiming tests passed when no validation was run.
