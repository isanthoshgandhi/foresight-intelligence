---
description: Run the full Foresight Engine pipeline with an expanded regional lens — auto-detects India, USA, Europe, or China and applies regional multipliers to signal scoring, surfacing local structural advantages and discounts in the report.
---

Run the full Foresight Engine pipeline with expanded regional analysis on: $ARGUMENTS

This is identical to `/foresight-engine:analyze` but with the regional lens explicitly expanded in the output.

**STEP 1 — VALIDATE INPUT**

Run: `python D:/Claude/foresight-engine/src/input_validator.py "$ARGUMENTS"`

If `valid` is false, display the rejection and stop.

**STEP 2 — COLLECT SIGNALS**

Use web_search to collect 18+ signals about: $ARGUMENTS

Run 6 searches with varied angles including region-specific searches:
1. Current state and recent data (with regional focus)
2. Supporting trends in the detected region
3. Opposing signals and regional headwinds
4. Regional policy, regulatory, and government actions
5. Regional technology and infrastructure factors
6. Historical precedents from the region or comparable regions

Classify each signal with `signal_type`, `steeep_category`, `temporal_layer`, `source`, `date`, `evidence_type`.

Write all signals to `D:/Claude/foresight-engine/signals.json`.

**STEP 3 — SCORE SIGNALS WITH REGIONAL MULTIPLIERS**

Run: `python D:/Claude/foresight-engine/src/signal_scorer.py D:/Claude/foresight-engine/signals.json`

The scorer auto-detects region from the query and applies regional multipliers from `D:/Claude/foresight-engine/contexts/`.

**STEP 4 — BUILD MATRIX**

Run: `python D:/Claude/foresight-engine/src/matrix_builder.py D:/Claude/foresight-engine/scored_signals.json`

**STEP 5 — FIND HISTORICAL ANALOGUES**

Prioritize analogues from the detected region or comparable regional situations. Write to `D:/Claude/foresight-engine/analogues.json`.

**STEP 6 — COMPUTE PROBABILITIES + CONFIDENCE**

Run: `python D:/Claude/foresight-engine/src/probability_calc.py D:/Claude/foresight-engine/scored_signals.json D:/Claude/foresight-engine/analogues.json`

Run: `python D:/Claude/foresight-engine/src/decision_guidance.py D:/Claude/foresight-engine/probabilities.json D:/Claude/foresight-engine/matrix.json D:/Claude/foresight-engine/scored_signals.json`

**STEP 7 — WRITE SCENARIOS**

Write four scenarios (PROBABLE, PLAUSIBLE, POSSIBLE, PREFERABLE) with regional context woven into each.

**STEP 8 — ASSEMBLE REPORT WITH EXPANDED REGIONAL LENS**

Output the full intelligence report (same format as `/foresight-engine:analyze`) PLUS an expanded Regional Lens section:

```
[REGIONAL LENS — DETECTED REGION]
Detected region: [India / USA / Europe / China / Global]
Top multipliers applied:
  [STEEEP/Temporal] [value]x — [reason from context notes]
  [STEEEP/Temporal] [value]x — [reason from context notes]
Key discounts applied:
  [STEEEP/Temporal] [value]x — [reason]
Key local variable: [structural factor unique to this region]
Regional context note: [1-2 sentences on how regional structure shapes this outcome]
```
