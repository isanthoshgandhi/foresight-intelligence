---
description: Run a fast Foresight Engine signal pulse — validate query, collect live signals, score STEEEP matrix, and compute probability distribution. No scenario writing. Target under 60 seconds.
---

Run the fast Foresight Engine signal pulse on: $ARGUMENTS

**STEP 1 — VALIDATE INPUT**

Run: `python D:/Claude/foresight-engine/src/input_validator.py "$ARGUMENTS"`

If `valid` is false, display the rejection and stop:
```
INVALID QUERY
Rule failed: [rule_failed]
Reason: [failure_reason]
Suggestion: [scope_note]
```

**STEP 2 — COLLECT SIGNALS**

Use web_search to collect 12+ signals about: $ARGUMENTS

Run 4 searches:
1. Current state and recent data
2. Supporting trends
3. Opposing signals and headwinds
4. Policy and market signals

Classify each signal with `signal_type` (SUPPORTING/OPPOSING/WILDCARD), `steeep_category`, `temporal_layer`, `source`, `date`, `evidence_type`.

Write to `D:/Claude/foresight-engine/signals.json`.

**STEP 3 — SCORE SIGNALS**

Run: `python D:/Claude/foresight-engine/src/signal_scorer.py D:/Claude/foresight-engine/signals.json`

**STEP 4 — BUILD MATRIX**

Run: `python D:/Claude/foresight-engine/src/matrix_builder.py D:/Claude/foresight-engine/scored_signals.json`

**STEP 6 — COMPUTE PROBABILITIES**

Run: `python D:/Claude/foresight-engine/src/probability_calc.py D:/Claude/foresight-engine/scored_signals.json D:/Claude/foresight-engine/analogues.json`

(Use empty analogues.json: `[]` if not present)

**OUTPUT — SIGNAL PULSE ONLY**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORESIGHT ENGINE — QUICK PULSE
[query]
Confidence: [confidence]/100 | Signals: [n] | [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
Supporting [n] [bar] | Opposing [n] [bar] | Wild [n]
Net: [direction]
Hot zone: [hottest_cell]

PROBABILITY DISTRIBUTION
■ PROBABLE  [pct%] [bar]
■ PLAUSIBLE [pct%] [bar]
■ POSSIBLE  [pct%] [bar]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run /foresight-engine:analyze for full scenarios and decision guidance.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
