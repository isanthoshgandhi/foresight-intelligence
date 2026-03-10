# /foresight-engine:region

**Usage:** `/foresight-engine:region [query]`

Run the full 8-step pipeline with an expanded Regional Lens section.

## What this command does

Identical to `/foresight-engine:analyze` but with:
- Regional context multipliers explicitly called out
- Top 2 multipliers that moved scores most — highlighted
- Key local variable — named explicitly
- Regional notes from context files surfaced in report

## Supported regions

| Region | Detected via keywords |
|--------|----------------------|
| India | india, indian, bharat, mumbai, delhi, bangalore, chennai, rupee |
| USA | usa, us, america, american, dollar, washington, silicon valley |
| Europe | europe, european, eu, euro, germany, france, uk, britain |
| China | china, chinese, beijing, shanghai, yuan, renminbi |
| Global | all other queries |

## Output

Full intelligence report PLUS expanded Regional Lens:
- Which multipliers amplified scores most
- Which multipliers discounted scores
- Key local structural variable
- Regional context notes from the context file

## Examples

```
/foresight-engine:region "Will India produce a $50B SaaS company by 2035?"
/foresight-engine:region "Will European green tech lead global markets by 2030?"
/foresight-engine:region "Will China surpass the US in AI by 2035?"
```

## Agent

Uses: `foresight-analyst` agent with regional expansion flag active.
