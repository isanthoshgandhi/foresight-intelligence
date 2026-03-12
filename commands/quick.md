---
description: "Get a fast read on any future question in under a minute — see how much evidence supports or opposes the outcome, with a quick probability estimate. Try: Will remote work become permanent by 2027? · Will India overtake China in manufacturing by 2030?"
argument-hint: "e.g. Will remote work become permanent by 2027?"
allowed-tools: Bash(python:*), WebSearch, WebFetch, Read, Write
---

Run a fast signal pulse on: $ARGUMENTS

**STEP 1 — VALIDATE**

!`python "${CLAUDE_PLUGIN_ROOT}/src/input_validator.py" "$ARGUMENTS"`

If `valid` is false, show rejection and stop.

**STEP 2 — COLLECT SIGNALS**

Use WebSearch to collect 12+ signals about: $ARGUMENTS

Run 4 searches: current state, supporting trends, opposing signals, policy/market signals.

Classify each: `signal_type`, `steeep_category`, `temporal_layer`, `source`, `date`, `evidence_type`.

Write to `${CLAUDE_PLUGIN_ROOT}/signals.json`.

**STEP 3 — SCORE**

!`python "${CLAUDE_PLUGIN_ROOT}/src/signal_scorer.py" "${CLAUDE_PLUGIN_ROOT}/signals.json"`

**STEP 4 — MATRIX**

!`python "${CLAUDE_PLUGIN_ROOT}/src/matrix_builder.py" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json"`

**STEP 5 — PROBABILITIES**

Create empty analogues file if needed: !`python -c "import json; open('${CLAUDE_PLUGIN_ROOT}/analogues.json','w').write('[]')"`

!`python "${CLAUDE_PLUGIN_ROOT}/src/probability_calc.py" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json" "${CLAUDE_PLUGIN_ROOT}/analogues.json"`

**OUTPUT**

Read `${CLAUDE_PLUGIN_ROOT}/probabilities.json` and `${CLAUDE_PLUGIN_ROOT}/matrix.json`, then output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORESIGHT ENGINE — QUICK PULSE
$ARGUMENTS
Confidence: [n]/100 | Signals: [n] | [today's date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
Supporting [n] [bar] | Opposing [n] [bar] | Wild [n]
Net: [direction]
Hot zone: [hottest_cell]

PROBABILITY DISTRIBUTION
■ PROBABLE  [n%] [████░░░░░░░░░░░░░░░░]
■ PLAUSIBLE [n%] [████░░░░░░░░░░░░░░░░]
■ POSSIBLE  [n%] [████░░░░░░░░░░░░░░░░]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run /analyze for full scenarios and decision guidance.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
