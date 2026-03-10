# /foresight-engine:analyze

**Usage:** `/foresight-engine:analyze [query]`

Run the full 8-step Foresight Engine pipeline.

## What this command does

1. Validates your query against 5 binary rules
2. Collects 18+ live signals via web search
3. Scores signals using a 4-factor deterministic formula
4. Builds the STEEEP × Temporal 18-cell matrix
5. Identifies 3 historical analogues via web search
6. Computes scenario probabilities and confidence score
7. Writes four crisp scenarios (Probable, Plausible, Possible, Preferable)
8. Assembles and outputs the complete intelligence report

## Output

Complete intelligence report including:
- Signal Pulse with supporting/opposing/wildcard breakdown
- Historical Match with best analogue
- Four scenarios with PROOF, IF, and BUT conditions
- THE ONE THING reframe
- Decision Guidance (stance, move, trigger)
- Regional Lens (if applicable)

## Examples

```
/foresight-engine:analyze "Will EVs dominate global cities by 2035?"
/foresight-engine:analyze "Will India produce a $50B SaaS company by 2035?"
/foresight-engine:analyze "Will China surpass the US in AI by 2035?"
```

## Agent

Uses: `foresight-analyst` agent for full orchestration.
