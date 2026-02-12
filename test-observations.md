# Skill Version Test Observations

Use this file to track behavior differences across skill versions when running test queries.

## Versions

| Version | Description | SKILL.md lines | Key changes |
|---------|-------------|----------------|-------------|
| Current (v1) | Original 708-line monolithic SKILL.md | 708 | Operating Guidelines truncated beyond ~200 lines |
| Matthew's | (Apply his plan directly) | TBD | TBD |
| Ours (v3) | Rewritten ~216-line SKILL.md + fixed references | 216 | Domain facts in context, grep/ping/cred fixes in refs, shared disk init added |

## Test Template

For each query, record:

```
### Q#: <query text>
**Version:** current / matthew / ours
**Files loaded:** (list reference files Claude read)
**Answer correct?** 0-3 scale (0=wrong, 1=partial, 2=correct but verbose, 3=correct+concise)
**Notes:** (what went right/wrong, any anti-patterns observed)
```

## Observations

### Round 1: Current (v1) — Baseline

_Run test queries against the original 708-line SKILL.md. Record results below._

### Round 2: Matthew's Version

_Apply Matthew's plan, run same queries. Record results below._

### Round 3: Ours (v3) — Target

_Run test queries against the rewritten SKILL.md + fixed references. Record results below._

## Comparison Summary

| Metric | Current (v1) | Matthew's | Ours (v3) |
|--------|-------------|-----------|-----------|
| Avg reads per query | | | |
| Avg score (0-3) | | | |
| Grep anti-patterns observed | | | |
| Auth anti-patterns observed | | | |
| Reference files loaded (total) | | | |
| Queries answered from SKILL.md alone | | | |

## Key Findings

_Fill in after testing all three versions._
