---
description: "Get a full strategic forecast for any future question — 4 scenarios, probability scores, and a clear action recommendation. Try: Will EVs dominate Indian cities by 2032? · Will AI replace junior engineers by 2027? · Will crypto replace banks by 2035?"
argument-hint: "e.g. Will EVs dominate Indian cities by 2032?"
allowed-tools: Bash(python:*), WebSearch, WebFetch, Read, Write
---

Run the full 8-step Foresight Engine pipeline on: $ARGUMENTS

**STEP 1 — VALIDATE INPUT**

!`python "${CLAUDE_PLUGIN_ROOT}/src/input_validator.py" "$ARGUMENTS"`

Parse the JSON output. If `valid` is false, display this and stop:
```
INVALID QUERY
Rule failed: [rule_failed]
Reason: [failure_reason]
Suggestion: [scope_note]
```

**STEP 2 — COLLECT SIGNALS**

Use WebSearch to collect 18+ real-world signals about: $ARGUMENTS

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
- `source`: domain name (e.g. reuters.com)
- `date`: publication date if available (YYYY-MM-DD)
- `evidence_type`: DATA, EVENT, ANALYSIS, or OPINION

Write all signals to `${CLAUDE_PLUGIN_ROOT}/signals.json`:
```json
[{"content": "...", "source": "...", "date": "YYYY-MM-DD", "signal_type": "SUPPORTING", "steeep_category": "Technological", "temporal_layer": "Strategic", "evidence_type": "DATA"}]
```

**STEP 3 — SCORE SIGNALS**

!`python "${CLAUDE_PLUGIN_ROOT}/src/signal_scorer.py" "${CLAUDE_PLUGIN_ROOT}/signals.json"`

Output: `${CLAUDE_PLUGIN_ROOT}/scored_signals.json`

**STEP 4 — BUILD MATRIX**

!`python "${CLAUDE_PLUGIN_ROOT}/src/matrix_builder.py" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json"`

Output: `${CLAUDE_PLUGIN_ROOT}/matrix.json`

**STEP 5 — FIND HISTORICAL ANALOGUES**

Use WebSearch to identify 3 real historical situations that closely parallel: $ARGUMENTS

For each analogue determine: name, description, conditions_then, tipping_incident, outcome, similarity_score (0-100).

Write to `${CLAUDE_PLUGIN_ROOT}/analogues.json`:
```json
[{"name": "...", "description": "...", "conditions_then": "...", "tipping_incident": "...", "outcome": "...", "similarity_score": 75}]
```

**STEP 6 — COMPUTE PROBABILITIES + CONFIDENCE**

!`python "${CLAUDE_PLUGIN_ROOT}/src/probability_calc.py" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json" "${CLAUDE_PLUGIN_ROOT}/analogues.json"`

Output: `${CLAUDE_PLUGIN_ROOT}/probabilities.json`

!`python "${CLAUDE_PLUGIN_ROOT}/src/decision_guidance.py" "${CLAUDE_PLUGIN_ROOT}/probabilities.json" "${CLAUDE_PLUGIN_ROOT}/matrix.json" "${CLAUDE_PLUGIN_ROOT}/scored_signals.json"`

Output: `${CLAUDE_PLUGIN_ROOT}/guidance.json`

**STEP 7 — WRITE SCENARIOS**

Read `${CLAUDE_PLUGIN_ROOT}/probabilities.json` and `${CLAUDE_PLUGIN_ROOT}/guidance.json`, then write four scenarios:

**PROBABLE [probable_pct%]** — Most likely path
- One sentence outcome
- PROOF: Specific real data point already supporting this direction
- IF: Key condition(s) that must hold
- BUT: Main friction or barrier

**PLAUSIBLE [plausible_pct%]** — Alternate path with real signal support
- One sentence outcome
- PROOF: Real data point showing this path exists
- IF: Condition(s) that would push toward this path
- BUT: What keeps it from being dominant

**POSSIBLE [possible_pct%]** — Lower-probability but real scenario
- One sentence outcome
- PROOF: Real incident or signal showing this risk
- IF: Trigger that would activate this scenario
- BUT: Why it remains unlikely

**PREFERABLE** — Normatively desired outcome (no probability)
- One sentence ideal outcome
- NEEDS: Two concrete structural changes required
- LEVERAGE: One high-leverage action that could unlock this path

**STEP 8 — OUTPUT REPORT**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORESIGHT ENGINE
$ARGUMENTS
Confidence: [n]/100 | Signals: [n] | [today's date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
Supporting [n] [████░░░░░░] | Opposing [n] [████░░░░░░] | Wild [n]
Net: [SUPPORTING LEADS / OPPOSING LEADS / NEUTRAL]
Hot zone: [hottest_cell from matrix.json]
Gap: [coldest cells]

HISTORICAL MATCH
[Best analogue name] ([similarity]% similar)
Tipped by: [tipping_incident]
Equivalent now: [EXISTS / ABSENT]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ PROBABLE [n%] — [Title]
[Outcome]
PROOF: [Data point]
IF: [Condition]
BUT: [Barrier]

■ PLAUSIBLE [n%] — [Title]
[Outcome]
PROOF: [Data point]
IF: [Condition]
BUT: [Barrier]

■ POSSIBLE [n%] — [Title]
[Outcome]
PROOF: [Data point]
IF: [Trigger]
BUT: [Why unlikely]

■ PREFERABLE — [Title]
[Ideal outcome]
NEEDS: [Two structural changes]
LEVERAGE: [High-leverage action]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ONE THING
[Single most critical pivot point — 1-2 sentences]
INCIDENT: [Real recent event proving this is the crux]
WATCH: [One specific milestone to monitor]
IF YES -> [Accelerating implication]
IF NO  -> [Stalling implication]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION GUIDANCE
Recommended stance: [from guidance.json recommended_stance]
Low-regret move: [from guidance.json low_regret_move]
Risk trigger: [from guidance.json risk_trigger]

[REGIONAL LENS — only if India/USA/Europe/China detected in query]
Top multipliers: [top 2 from regional_context]
Key local variable: [from context notes]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
