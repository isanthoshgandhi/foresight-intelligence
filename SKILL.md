# Foresight Engine — Personal Skill
Author: Santhosh Gandhi | github.com/isanthoshgandhi/foresight-engine

---

## ⚠️ Limitations of This Skill vs the Full Plugin

This SKILL.md is an instruction layer, not a program. Understand the tradeoffs
before using it for high-stakes decisions:

| Capability | Claude Code Plugin | MCP Server | This Skill |
|------------|-------------------|------------|------------|
| Arithmetic engine | Python (deterministic) | Python (deterministic) | LLM reasoning (approximate) |
| Score reproducibility | Identical every run | Identical every run | ±2-5% variance per run |
| Regional multipliers | Exact float multiplication | Exact float multiplication | Claude approximates |
| Probability normalization | Forces sum = 100% | Forces sum = 100% | May drift ±1-3% |
| Signal batch scoring | Loops all signals in code | Loops all signals in code | Claude may summarize, not loop |
| Matrix cell computation | All 18 cells computed | All 18 cells computed | Claude may skip low-signal cells |
| Web search | Real-time via Claude Code | Real-time via Claude tools | Real-time (claude.ai Pro only) |
| Audit trail | Python logs available | JSON tool call logs | None — reasoning is implicit |

**When to use this Skill:**
- Exploratory analysis, content creation, quick foresight checks
- When you don't have Claude Code or a local Python environment
- When approximate outputs are acceptable

**When NOT to use this Skill:**
- Investment memos or high-stakes decisions requiring exact reproducibility
- When you need to audit or verify the scoring math
- When running batch analyses that need consistent outputs

**The honest truth:** For VC-grade analysis, use the Claude Code plugin or MCP
server. This Skill produces structurally correct reports but the numbers are
Claude's best approximation, not computed ground truth.

---

## Trigger Phrases

Activate this skill when the user's message contains any of:
- "foresight analysis"
- "scenario analysis"
- "foresight engine"
- Any question of the form "Will [X] by [year]?"
- Requests for STEEEP analysis, futures cone, or structured signal analysis

---

## The 8-Step Pipeline

Execute ALL 8 steps in order. Do not skip steps. Do not combine steps. Show your work for each step.

---

### Step 1 — Validate Input

Apply exactly 5 binary rules. If ANY rule fails, stop and explain why. Do not proceed.

**Rule 1 — Entity Reality:** Does the entity in the question actually exist in the real world? Fail if the entity is fictional, hypothetical, or unnamed (e.g. "a startup", "some company").

**Rule 2 — System Existence:** Is the system or domain referenced actually observable and researchable? Fail if the question is purely philosophical or metaphysical with no empirical signals.

**Rule 3 — Time Horizon:** Does the question specify a year or decade? Fail if no time horizon is given. A valid time horizon is 2 to 30 years from today.

**Rule 4 — Signal Availability:** Could real-world evidence (news, research, policy, market data) plausibly exist for this topic? Fail if the topic is classified, completely speculative, or has no published discourse.

**Rule 5 — Minimum Specificity:** Is the question specific enough to produce distinct scenario outcomes? Fail if the question is so broad that any answer is trivially true (e.g. "Will technology change by 2050?").

Output format:
```
VALIDATION
Rule 1 Entity Reality:    PASS / FAIL — [reason]
Rule 2 System Existence:  PASS / FAIL — [reason]
Rule 3 Time Horizon:      PASS / FAIL — [reason]
Rule 4 Signal Availability: PASS / FAIL — [reason]
Rule 5 Specificity:       PASS / FAIL — [reason]
Result: PROCEED / STOP
```

---

### Step 2 — Collect Signals

Run exactly 6 web searches. Collect a minimum of 18 signals total across all searches. Do not proceed with fewer than 18.

**Search 1:** Current state — "[topic] current status [year]"
**Search 2:** Growth indicators — "[topic] growth data market size [year]"
**Search 3:** Barriers and headwinds — "[topic] challenges barriers risks"
**Search 4:** Policy and regulation — "[topic] government policy regulation [region]"
**Search 5:** Technology or infrastructure enablers — "[topic] technology infrastructure investment"
**Search 6:** Historical precedent — "[topic] historical analogue similar transition"

For each signal collected, classify all 6 attributes:

| Attribute | Values |
|---|---|
| direction | supporting / opposing / wildcard / neutral |
| steeep_category | Social / Technological / Economic / Environmental / Ethical / Political |
| temporal_layer | Operational (0-2 yr) / Strategic (2-10 yr) / Civilizational (10+ yr) |
| source_type | primary (official/government data) / secondary (established news, industry reports) / opinion (commentary, prediction) |
| recency_days | integer — days since published |
| has_evidence | true (contains a number, date, or measurable fact) / false |

Present signals in a table with all 6 columns filled for every row.

---

### Step 3 — Score Signals

Score every signal individually using this exact formula:

```
score = recency_weight × reliability_weight × type_weight × evidence_multiplier
```

Cap the result at 1.0. Round to 2 decimal places.

**Recency weights (by recency_days):**
- 0–90 days: 1.00
- 91–365 days: 0.80
- 366–1095 days (1-3 yr): 0.60
- 1095+ days (3+ yr): 0.40
- unknown date: 0.50

**Reliability weights (by source_type):**
- primary (government/official): 1.00
- established news (Reuters, Bloomberg, FT, ET): 0.90
- industry report (McKinsey, Gartner, NASSCOM): 0.85
- analyst commentary: 0.70
- opinion/blog/social: 0.50
- unknown: 0.40

**Type weights (by direction):**
- supporting: 1.00
- opposing: 1.00 (opposing evidence is equally important — never discount it)
- neutral: 0.60
- wildcard: 1.30 (high impact even if uncertain)

**Evidence multiplier (by evidence_type):**
- DATA or STATISTIC: × 1.20
- EVENT or INCIDENT: × 1.00
- ANALYSIS or OPINION: × 0.70 (default when unknown)

Apply regional multipliers AFTER computing the base score:
```
final_score = min(1.0, base_score × regional_multiplier[steeep_category][temporal_layer])
```

Show a scoring table with columns: Signal (short label) | recency_w | reliability_w | type_w | evidence_mult | base_score | regional_mult | final_score

---

### Step 4 — Build 6×3 STEEEP×Temporal Matrix

Populate all 18 cells of the matrix. Each cell value = average final_score of all signals mapped to that STEEEP × Temporal combination. If no signals map to a cell, its value = 0.

**Matrix layout:**

|  | Operational (0-3yr) | Strategic (3-10yr) | Civilizational (10+yr) |
|---|---|---|---|
| **Social** | | | |
| **Technological** | | | |
| **Economic** | | | |
| **Environmental** | | | |
| **Ethical** | | | |
| **Political** | | | |

Fill every cell. Then identify:
- **hot_zones:** cells with score > 0.50
- **gap_zones:** cells with score = 0.00 (no signals)
- **dominant zone:** the single highest-scoring cell

Apply regional multipliers to each cell value using the table in the Regional Context section.

---

### Step 5 — Find 3 Historical Analogues

Search for and identify exactly 3 real historical cases that parallel the question's trajectory. For each analogue state:

1. **Name:** Common name of the historical transition
2. **Similarity (%):** Your estimated % similarity to the current question (0–100)
3. **Tipping event:** The single event or policy that caused the transition to accelerate
4. **Equivalent today:** Does an equivalent tipping event exist in the current context? (YES / NO / PARTIAL)

Prefer analogues with similarity ≥ 60%. If no analogue exceeds 60%, note this as a confidence penalty.

---

### Step 6 — Compute Probabilities and Confidence

#### Probability Computation

Assign raw scores to the three probability-eligible scenarios:

```
R_probable  = (count of supporting signals with score > 0.70) × 3
            + (best analogue similarity / 100) × 4
            + (count of hot_zones) × 2

R_plausible = (count of supporting signals with score 0.40–0.70) × 2
            + (second-best analogue similarity / 100) × 3

R_possible  = (count of wildcard signals) × 2
            + (count of opposing signals with score > 0.60) × 2
            + (count of gap_zones / 18) × 3
```

Normalize to sum to exactly 100%:
```
total = R_probable + R_plausible + R_possible
probable_pct  = round(R_probable  / total × 100, 1)
plausible_pct = round(R_plausible / total × 100, 1)
possible_pct  = 100 - probable_pct - plausible_pct
```

#### Confidence Score Computation

Compute confidence as a weighted 4-factor average (0–100):

```
signal_count_score  = min(100, total_signals / 25 × 100)   × 0.30
signal_diversity    = (unique STEEEP categories covered / 6) × 100 × 0.30
recency_score       = (signals with recency_days ≤ 90 / total_signals) × 100 × 0.20
evidence_score      = (signals with has_evidence=true / total_signals) × 100 × 0.20

confidence = round(signal_count_score + signal_diversity + recency_score + evidence_score)
```

Cap at 100. Do not round intermediate values until the final integer.

---

### Step 7 — Write Scenarios

Write four scenario blocks. Each is distinct and must not overlap in narrative.

**PROBABLE** — The most likely trajectory given current signals. Base on the highest-probability outcome.

**PLAUSIBLE** — A credible alternative path. Not the default, but well-supported.

**POSSIBLE** — A low-probability but non-zero outcome. Must be coherent, not absurd.

**PREFERABLE** — The best outcome worth designing toward. Not probability-weighted. State what conditions would need to be created.

For PROBABLE, PLAUSIBLE, and POSSIBLE, include:
- **Narrative:** 2–3 sentence description. No hedging language ("might", "could"). Write as if describing the future as it unfolds.
- **PROOF:** One line. Must contain a number, date, or named fact. Format: "PROOF: [fact with number/date]."
- **IF:** One line. The condition that makes this scenario activate. Format: "IF: [condition]."
- **BUT:** One line. The friction point or bottleneck. Format: "BUT: [constraint]."

For PREFERABLE:
- **Narrative:** 2–3 sentences describing the desired state.
- **NEEDS:** What must be true for this to happen (policy, capital, technology, behavior).
- **LEVERAGE:** The single highest-leverage intervention available today.

**THE ONE THING** block: After the four scenarios, identify the single variable that determines which scenario actually happens. Format:
```
THE ONE THING
[One sentence naming the variable.]
INCIDENT: [A real past event showing this variable's power]
WATCH: [The leading indicator to monitor — a milestone, metric, or policy action]
IF YES → [What accelerates]
IF NO  → [What stalls]
```

---

### Step 8 — Assemble Report

Output the complete report using this exact template. Use `━` characters for dividers. Do not add extra sections. Do not write prose outside the template.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORESIGHT ENGINE
[Query]
Confidence: [X]/100 | Signals: [N] | [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
Supporting [N] [████████████░░░░░░░░] | Opposing [N] [████░░░░░░░░░░░░░░░░] | Wild [N]
Net: [SUPPORTING LEADS / OPPOSING LEADS / NEUTRAL]
Hot zone: [top 1-2 hot zone names]
Gap: [top 1-2 gap zone names, or "None — full coverage"]

HISTORICAL MATCH
[Best analogue name] ([similarity]% similar)
Tipped by: [tipping event description]
Equivalent now: [EXISTS / PARTIAL / ABSENT]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ PROBABLE [[X]%] — [Short title]
[2-3 sentence narrative]
PROOF: [fact with number or date]
IF: [activation condition]
BUT: [constraint]

■ PLAUSIBLE [[X]%] — [Short title]
[2-3 sentence narrative]
PROOF: [fact with number or date]
IF: [activation condition]
BUT: [constraint]

■ POSSIBLE [[X]%] — [Short title]
[2-3 sentence narrative]
PROOF: [fact with number or date]
IF: [activation condition]
BUT: [constraint]

■ PREFERABLE — [Short title]
[2-3 sentence narrative]
NEEDS: [conditions required]
LEVERAGE: [highest-leverage intervention]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ONE THING
[One sentence naming the key variable]
INCIDENT: [past event]
WATCH: [leading indicator]
IF YES → [accelerant]
IF NO  → [stall]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION GUIDANCE
Recommended stance: [stance from compute_stance logic below]
Low-regret move: [action that pays off in multiple scenarios]
Risk trigger: [the specific signal that would invalidate the probable scenario]

[REGIONAL LENS — [REGION]]
Top multipliers: [steeep/temporal (Xx)] [steeep/temporal (Xx)]
Key local variable: [one sentence on the dominant local structural factor]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Signal pulse bar:** Each `█` represents 5% of the max count. Use 20 characters total per bar (`█` filled + `░` empty).

---

## Regional Context

Apply these multipliers in Step 3 and Step 4. Multipliers > 1.0 amplify signals in that cell. Multipliers < 1.0 discount them.

### India

| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.10 | 1.30 | 1.20 |
| **Technological** | 1.40 | 1.30 | 1.10 |
| **Economic** | 1.20 | 1.25 | 1.15 |
| **Environmental** | 0.90 | 1.00 | 1.10 |
| **Ethical** | 0.95 | 1.00 | 1.05 |
| **Political** | 0.85 | 0.90 | 1.00 |

**India context note:** UPI/DPI infrastructure gives India asymmetric advantage in Technological/Operational signals. Mobile-first adoption and deep software talent amplify Technological signals. Political/Operational is discounted due to regulatory fragmentation across states.

### USA

| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.00 | 1.10 | 1.05 |
| **Technological** | 1.20 | 1.40 | 1.20 |
| **Economic** | 1.10 | 1.30 | 1.10 |
| **Environmental** | 0.95 | 1.00 | 1.05 |
| **Ethical** | 1.05 | 1.10 | 1.10 |
| **Political** | 0.90 | 0.95 | 1.00 |

**USA context note:** Deep capital markets and Silicon Valley ecosystem amplify Technological/Strategic signals. Political/Operational is discounted by legislative gridlock.

### Europe

| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.00 | 1.05 | 1.10 |
| **Technological** | 1.00 | 1.10 | 1.05 |
| **Economic** | 0.95 | 0.90 | 0.90 |
| **Environmental** | 1.20 | 1.40 | 1.30 |
| **Ethical** | 1.10 | 1.20 | 1.20 |
| **Political** | 1.05 | 1.10 | 1.10 |

**Europe context note:** Regulatory leadership (GDPR, EU AI Act, Green Deal) amplifies Environmental/Strategic signals significantly. Economic/Civilizational is discounted by structural demographic headwinds and energy dependency.

### China

| | Operational | Strategic | Civilizational |
|---|---|---|---|
| **Social** | 1.00 | 1.10 | 1.05 |
| **Technological** | 1.20 | 1.50 | 1.30 |
| **Economic** | 1.10 | 1.20 | 1.10 |
| **Environmental** | 0.90 | 1.00 | 1.05 |
| **Ethical** | 0.70 | 0.75 | 0.80 |
| **Political** | 1.10 | 1.15 | 1.00 |

**China context note:** State-directed capital and industrial policy amplify Technological/Strategic signals strongly. Ethical/Operational is heavily discounted due to limited transparency and constrained civil discourse.

### Global (default)

All multipliers = 1.0. Apply when no region is detectable from the query.

---

## Quick Mode Instructions

When the user requests "quick" mode or uses `/foresight-engine:quick`:

1. Execute Steps 1–4 only (Validate, Collect, Score, Matrix).
2. Skip Steps 5–7 (Analogues, Scenarios, THE ONE THING).
3. Run Step 6b (Confidence) using available signals.
4. Output: Signal Pulse block + Matrix summary + Confidence score only.
5. Add a note: "Quick mode — no scenarios written. Run full analysis for PROBABLE/PLAUSIBLE/POSSIBLE/PREFERABLE."

Target time: under 60 seconds of Claude reasoning.

---

## Region Mode Instructions

When the user requests "region" mode or uses `/foresight-engine:region`:

1. Execute all 8 steps of the full pipeline.
2. In Step 4, apply the full regional multiplier table (do not use global defaults).
3. In Step 8, expand the REGIONAL LENS section to include:
   - Full multiplier table for the detected region
   - Top 3 amplified cells and their scores
   - Top 2 discounted cells and their scores
   - A 3-sentence structural analysis of why this region amplifies or discounts these signals
4. Everything else is identical to full mode.

---

## Compute Stance Logic

Use this decision tree to generate the "Recommended stance" in the DECISION GUIDANCE block:

```
IF probable_pct > 50:
    stance = "Align with probable scenario trajectory"
    low_regret = "Invest in capability building in the dominant hot zone"

ELIF plausible_pct > 35:
    stance = "Hedge between probable and plausible scenarios"
    low_regret = "Build optionality — choose reversible commitments that work in both"

ELIF possible_pct > 25:
    stance = "Maintain optionality — signal environment is ambiguous"
    low_regret = "Invest in monitoring and early-warning indicators"

ELSE:
    stance = "Defer commitment — insufficient signal clarity"
    low_regret = "Focus on reducing uncertainty before acting"
```

**Confidence qualifier:**
- confidence ≥ 70: Add "High conviction —" before stance
- confidence 40–69: No prefix (default)
- confidence < 40: Add "Low conviction — " before stance and note: "Expand signal collection before acting"

**Risk trigger:** Identify the single opposing signal with the highest final_score and state it as the risk trigger. Format: "[Signal content] could invalidate the probable scenario if [condition]."
