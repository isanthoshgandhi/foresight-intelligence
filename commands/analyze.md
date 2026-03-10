---
description: Run the full Foresight Engine pipeline — validate query, collect live signals, score STEEEP matrix, find historical analogues, compute probabilities, and produce a four-scenario intelligence report with decision guidance.
---

Run the full 8-step Foresight Engine pipeline on the query: $ARGUMENTS

**STEP 1 — VALIDATE INPUT**

Run: `python D:/Claude/foresight-engine/src/input_validator.py "$ARGUMENTS"`

Parse the JSON output. If `valid` is false, display the rejection message and stop:
```
INVALID QUERY
Rule failed: [rule_failed]
Reason: [failure_reason]
Suggestion: [scope_note]
```

**STEP 2 — COLLECT SIGNALS**

Use web_search to collect 18+ real signals about: $ARGUMENTS

Run 6 searches with varied angles:
1. Current state and recent data
2. Supporting trends and positive signals
3. Opposing signals and headwinds
4. Policy, regulatory, and government actions
5. Technology and infrastructure factors
6. Historical precedents and analogues

For each signal found, classify:
- `signal_type`: SUPPORTING, OPPOSING, or WILDCARD
- `steeep_category`: Social, Technological, Economic, Environmental, Ethical, or Political
- `temporal_layer`: Operational (0-2yr), Strategic (2-10yr), or Civilizational (10-30yr)
- `source`: domain name (e.g. reuters.com, mckinsey.com)
- `date`: publication date if available
- `evidence_type`: DATA, EVENT, ANALYSIS, or OPINION

Write all signals to `D:/Claude/foresight-engine/signals.json` in this format:
```json
[{"content": "...", "source": "...", "date": "YYYY-MM-DD", "signal_type": "SUPPORTING", "steeep_category": "Technological", "temporal_layer": "Strategic", "evidence_type": "DATA"}]
```

**STEP 3 — SCORE SIGNALS**

Run: `python D:/Claude/foresight-engine/src/signal_scorer.py D:/Claude/foresight-engine/signals.json`

This produces `D:/Claude/foresight-engine/scored_signals.json`.

**STEP 4 — BUILD MATRIX**

Run: `python D:/Claude/foresight-engine/src/matrix_builder.py D:/Claude/foresight-engine/scored_signals.json`

This produces `D:/Claude/foresight-engine/matrix.json`.

**STEP 5 — FIND HISTORICAL ANALOGUES**

Use web_search to identify 3 real historical situations that closely parallel: $ARGUMENTS

For each analogue, determine:
- `name`: Short label (e.g. "South Korea EV adoption 2016-2022")
- `description`: One sentence summary
- `conditions_then`: What conditions existed at the time
- `tipping_incident`: The single event that tipped the outcome
- `outcome`: What actually happened
- `similarity_score`: 0-100 score of how closely it matches this question

Write to `D:/Claude/foresight-engine/analogues.json`:
```json
[{"name": "...", "description": "...", "conditions_then": "...", "tipping_incident": "...", "outcome": "...", "similarity_score": 75}]
```

**STEP 6 — COMPUTE PROBABILITIES + CONFIDENCE**

Run: `python D:/Claude/foresight-engine/src/probability_calc.py D:/Claude/foresight-engine/scored_signals.json D:/Claude/foresight-engine/analogues.json`

This produces `D:/Claude/foresight-engine/probabilities.json` with `probable_pct`, `plausible_pct`, `possible_pct`, and `confidence`.

Also run: `python D:/Claude/foresight-engine/src/decision_guidance.py D:/Claude/foresight-engine/probabilities.json D:/Claude/foresight-engine/matrix.json D:/Claude/foresight-engine/scored_signals.json`

This produces `D:/Claude/foresight-engine/guidance.json`.

**STEP 7 — WRITE SCENARIOS**

Using the signal data, matrix hottest cell, probabilities, and historical analogues — write four scenarios:

**PROBABLE [probable_pct%]** — The most likely path given current signals
- One sentence describing the outcome
- PROOF: A real, specific data point that already supports this direction
- IF: The key condition(s) that must hold for this to unfold
- BUT: The friction or barrier that could slow it

**PLAUSIBLE [plausible_pct%]** — An alternate path with real signal support
- One sentence describing the outcome
- PROOF: A real data point showing this path exists
- IF: The condition(s) that would push toward this path
- BUT: What keeps it from being the dominant scenario

**POSSIBLE [possible_pct%]** — A lower-probability but real scenario
- One sentence describing the outcome
- PROOF: A real incident or signal showing this risk exists
- IF: The trigger that would activate this scenario
- BUT: Why it remains unlikely

**PREFERABLE** — The normatively desired outcome (no probability)
- One sentence describing the ideal outcome
- NEEDS: Two concrete structural changes required
- LEVERAGE: One high-leverage action that could unlock this path

**STEP 8 — ASSEMBLE REPORT**

Output the complete report in this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORESIGHT ENGINE
[query]
Confidence: [confidence]/100 | Signals: [total_signals] | [date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
Supporting [n] [bar] | Opposing [n] [bar] | Wild [n]
Net: [SUPPORTING LEADS / OPPOSING LEADS / NEUTRAL]
Hot zone: [hottest_cell]
Gap: [coldest cells]

HISTORICAL MATCH
[Best analogue name] ([similarity]% similar)
Tipped by: [tipping_incident]
Equivalent now: [EXISTS / ABSENT]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ PROBABLE [probable_pct%] — [Title]
[One sentence outcome]
PROOF: [Specific data point]
IF: [Condition(s)]
BUT: [Barrier]

■ PLAUSIBLE [plausible_pct%] — [Title]
[One sentence outcome]
PROOF: [Specific data point]
IF: [Condition(s)]
BUT: [Barrier]

■ POSSIBLE [possible_pct%] — [Title]
[One sentence outcome]
PROOF: [Specific data point]
IF: [Trigger]
BUT: [Why unlikely]

■ PREFERABLE — [Title]
[One sentence ideal outcome]
NEEDS: [Two structural changes]
LEVERAGE: [One high-leverage action]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ONE THING
[Single most critical pivot point or reframe — 1-2 sentences]
INCIDENT: [A real recent event that proves this is the crux]
WATCH: [One specific milestone to monitor]
IF YES -> [Accelerating implication]
IF NO -> [Stalling implication]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION GUIDANCE
Recommended stance: [from guidance.json]
Low-regret move: [from guidance.json]
Risk trigger: [from guidance.json]

[REGIONAL LENS — if region detected]
Top multipliers: [top 2 from regional_context]
Key local variable: [from context notes]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
