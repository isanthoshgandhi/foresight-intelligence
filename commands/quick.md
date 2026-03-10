# /foresight-engine:quick

**Usage:** `/foresight-engine:quick [query]`

Run a fast partial Foresight Engine pipeline. Target: under 60 seconds.

## What this command does

Runs Steps 1–4 + Step 6 only:
1. Validates your query (Step 1)
2. Collects signals via web search (Step 2)
3. Scores signals (Step 3)
4. Builds STEEEP × Temporal matrix (Step 4)
5. Computes probabilities and confidence (Step 6)

**Does NOT run:**
- Historical analogue search (Step 5)
- Scenario writing (Step 7)
- Full report assembly (Step 8)

## Output

Signal Pulse section only:
- Supporting / Opposing / Wildcard signal counts
- Net direction
- Hot zone identification
- Probability distribution (Probable / Plausible / Possible %)
- Confidence score

No scenarios written. No full report.

## When to use

- Initial signal check before deep analysis
- Quick gut-check on a topic
- When you need signal direction fast

## Examples

```
/foresight-engine:quick "Will Indian fintech dominate SEA by 2030?"
/foresight-engine:quick "Is quantum computing a near-term threat to encryption?"
```

## Agent

Uses: `foresight-analyst` agent in abbreviated mode (Steps 1–4 + 6 only).
