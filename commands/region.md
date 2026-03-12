---
description: "Full strategic forecast with deep regional context. Mention a region and get analysis shaped by what is structurally unique to that market. Try: Will US tech regulation fragment the internet by 2030? · Will Europe lead the green energy transition by 2035?"
argument-hint: "e.g. Will US tech regulation fragment the internet by 2030?"
allowed-tools: Bash(python:*), WebSearch, WebFetch, Read, Write
---

Run the full Foresight Engine pipeline with expanded regional lens on: $ARGUMENTS

This is identical to /analyze but with the regional multipliers explicitly surfaced and explained in the output.

**STEP 1 — VALIDATE**

!`python "${CLAUDE_PLUGIN_ROOT}/src/input_validator.py" "$ARGUMENTS"`

If `valid` is false, show rejection and stop.

**STEP 2 — COLLECT SIGNALS (REGION-FOCUSED)**

Use WebSearch to collect 18+ signals about: $ARGUMENTS

Run 6 searches with regional focus:
1. Current state and data in the detected region
2. Regional supporting trends
3. Regional headwinds and opposing signals
4. Regional policy and regulatory actions
5. Regional technology and infrastructure
6. Historical analogues from or comparable to the region

Classify each: `signal_type`, `steeep_category`, `temporal_layer`, `source`, `date`, `evidence_type`.

Write to `${CLAUDE_PLUGIN_ROOT}/signals.json`.

**STEP 3 — SCORE WITH REGIONAL MULTIPLIERS**

!`python "${CLAUDE_PLUGIN_ROOT}/src/signal_scorer.py" "${CLAUDE_PLUGIN_ROOT}/signals.json"`

The scorer auto-detects the region and applies multipliers from `${CLAUDE_PLUGIN_ROOT}/contexts/`.

**STEP 4 — MATRIX**

!`python "${CLAUDE_PLUGIN_ROOT}/src/matrix_builder.py" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json"`

**STEP 5 — HISTORICAL ANALOGUES (REGION-PRIORITIZED)**

Find 3 historical analogues, prioritizing examples from or comparable to the detected region.

Write to `${CLAUDE_PLUGIN_ROOT}/analogues.json`.

**STEP 6 — PROBABILITIES + GUIDANCE**

!`python "${CLAUDE_PLUGIN_ROOT}/src/probability_calc.py" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json" "${CLAUDE_PLUGIN_ROOT}/analogues.json"`

!`python "${CLAUDE_PLUGIN_ROOT}/src/decision_guidance.py" "${CLAUDE_PLUGIN_ROOT}/probabilities.json" "${CLAUDE_PLUGIN_ROOT}/matrix.json" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json"`

**STEP 7 — WRITE SCENARIOS** (with regional context woven into each)

**STEP 8 — OUTPUT FULL REPORT + EXPANDED REGIONAL LENS**

Output the complete report (same as /analyze) PLUS this expanded section:

```
[REGIONAL LENS — EXPANDED]
Detected region: [India / USA / Europe / China / Global]

Top multipliers applied:
  [STEEEP/Temporal] [value]x — [why this region has an advantage here]
  [STEEEP/Temporal] [value]x — [why this region has an advantage here]

Discounts applied:
  [STEEEP/Temporal] [value]x — [structural weakness or friction]

Key local variable: [one structural factor unique to this region]
Regional insight: [1-2 sentences on how regional structure shapes this outcome]
```
