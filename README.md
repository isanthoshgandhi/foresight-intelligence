# Foresight Engine

**Claude Code Plugin — v1.2.0**
Author: Santhosh Gandhi | GitHub: [github.com/isanthoshgandhi](https://github.com/isanthoshgandhi)

---

## What It Does

Foresight Engine is a strategic intelligence plugin for Claude Code. Give it any real-world question about the future — a sector, a technology, a geopolitical shift — and it produces a structured four-scenario analysis backed by live signals, historical analogues, and deterministic probability scoring.

It augments Claude's native capabilities with a structured methodology layer inspired by IFTF foresight practices (Futures Cone, STEEEP, Cross-Impact Analysis, Backcasting). The result is a crisp intelligence report you can act on.

---

## Two-Layer Architecture

This plugin has two layers that must **never** be confused:

| **Claude Native Layer** (called, never coded) | **Plugin Code Layer** (deterministic arithmetic only) |
|------------------------------------------------|-------------------------------------------------------|
| `web_search` → find real-world signals         | `input_validator.py` → 5 binary rules                |
| `web_fetch` → read full source articles        | `signal_scorer.py` → 4-factor scoring formula        |
| Reasoning → identify historical analogues      | `matrix_builder.py` → 18-cell STEEEP×Temporal grid   |
| Language → write scenario narratives           | `regional_context.py` → multiplier routing            |
| Judgment → classify signals and sources        | `probability_calc.py` → normalizes scores to 100%    |
|                                                | `confidence_calc.py` → weighted average formula       |
|                                                | `decision_guidance.py` → strategic stance computation |
|                                                | `report_formatter.py` → enforces crisp template       |

**Core rule:** Python code NEVER calls web_search, generates narrative, or simulates reasoning. Claude NEVER does arithmetic or probability calculations.

---

## The 8-Step Pipeline

1. **Validate Input** — 5 binary rules check query is real, specific, and analyzable
2. **Collect Signals** — Claude runs 6 web searches, collects 18+ signals, classifies each
3. **Score Signals** — Python scores: `recency × reliability × type × evidence` (capped at 1.0)
4. **Build Matrix** — Python populates the 6×3 STEEEP×Temporal 18-cell grid
5. **Find Historical Analogues** — Claude identifies 3 real historical parallels via web search
6. **Compute Probabilities + Confidence** — Python normalizes to 100%, computes 0-100 confidence score
7. **Write Scenarios** — Claude writes four crisp scenarios with PROOF, IF, and BUT conditions
8. **Assemble Report** — Python slots everything into the crisp template

---

## Installation

```bash
# Install locally
claude plugin add ./foresight-engine

# Verify installation
claude plugin list
```

**Requirements:** Python 3.10+, pytest (for tests), git 2.x

---

## Usage

### `/foresight-engine:analyze` — Full pipeline

```
/foresight-engine:analyze "Will EVs dominate global cities by 2035?"
/foresight-engine:analyze "Will India produce a $50B SaaS company by 2035?"
/foresight-engine:analyze "Will China surpass the US in AI by 2035?"
```

### `/foresight-engine:quick` — Signal pulse only (fast)

```
/foresight-engine:quick "Will Indian fintech dominate SEA by 2030?"
/foresight-engine:quick "Is quantum computing a near-term threat to encryption?"
```

Runs Steps 1–4 + 6 only. No scenario writing. Target: under 60 seconds.

### `/foresight-engine:region` — Full pipeline with expanded regional lens

```
/foresight-engine:region "Will Indian B2B SaaS produce a $50B company by 2035?"
/foresight-engine:region "Will European green tech lead global markets by 2030?"
```

---

## Sample Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORESIGHT ENGINE
Will EVs dominate Indian cities by 2032?
Confidence: 62/100 | Signals: 19 | 2026-03-11
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SIGNAL PULSE
Supporting 11 [████████████░░░░░░░░] | Opposing 4 [████░░░░░░░░░░░░░░░░] | Wild 2
Net: SUPPORTING LEADS
Hot zone: Technological/Strategic
Gap: Ethical/Civilizational, Environmental/Operational

HISTORICAL MATCH
South Korea EV rollout 2016-2022 (78% similar)
Tipped by: 2019 Hyundai IONIQ subsidy tripling caused 300% YoY EV sales jump
Equivalent now: EXISTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

■ PROBABLE [54%] — Gradual EV Dominance
India EV penetration reaches 25-30% of new city sales by 2032, led by 2W/3W.
PROOF: FAME-II scheme disbursed ₹10,000 Cr subsidies; 2W EV share hit 5.8% in 2024.
IF: Battery costs drop below $80/kWh AND charging infra reaches 50K stations.
BUT: Grid reliability and upfront cost remain barriers in Tier 2/3 cities.

■ PLAUSIBLE [32%] — Patchy Adoption
EVs dominate 2W/3W but cars lag; city-to-city variance is high by 2032.
PROOF: Delhi EV share 12% vs national 4% — 3x variance already visible in 2025.
IF: State-level policy remains fragmented without national grid mandate.
BUT: Strong corporate fleet conversion could accelerate without retail adoption.

■ POSSIBLE [14%] — Disruption Stall
EV adoption stalls below 10% due to grid failures, battery fire incidents, or policy reversal.
PROOF: 2022 Ola/Okinawa fire incidents caused 15% demand drop in Q3 2022.
IF: Multiple high-profile battery safety incidents trigger regulatory freeze.
BUT: Unlikely given FAME-III momentum and global supply cost declines.

■ PREFERABLE — Accelerated Clean Transition
India reaches 40%+ EV penetration across all categories by 2032.
NEEDS: National grid upgrade policy + GST parity on EV components.
LEVERAGE: Mandate EV-only procurement for all government and PSU fleets by 2028.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

THE ONE THING
The question is not whether EVs will grow — it is whether India's grid can absorb the load.
INCIDENT: Tamil Nadu grid collapse during EV charging surge pilot, 2024
WATCH: RBI/Ministry charging infra bond issuance milestone
IF YES -> EV adoption accelerates 2x faster than current trajectory
IF NO -> Adoption stalls in Tier 1, never breaks through to Tier 2/3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DECISION GUIDANCE
Recommended stance: Align with probable scenario trajectory
Low-regret move: Invest in technology capability building — signals favor accelerated commitment
Risk trigger: Battery fire incidents in India caused 15% demand drop in Q3 2022

[REGIONAL LENS — INDIA]
Top multipliers: Technological/Operational (1.40x), Technological/Strategic (1.30x)
Key local variable: UPI/DPI infrastructure advantage amplifies Technological/Operational signals
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Regional Context

The plugin applies regional multipliers to adjust signal scores for local structural factors.

| Region | Detected Via | Key Advantage | Key Discount |
|--------|-------------|---------------|--------------|
| **India** | india, rupee, mumbai, upi... | Technological/Operational (1.4x) | Political/Operational (0.85x) |
| **USA** | usa, america, silicon valley... | Technological/Strategic (1.4x) | Political/Operational (0.9x) |
| **Europe** | europe, eu, germany, gdpr... | Environmental/Strategic (1.4x) | Economic/Civilizational (0.9x) |
| **China** | china, beijing, yuan... | Technological/Strategic (1.5x) | Ethical/Operational (0.7x) |
| **Global** | (all other queries) | All multipliers = 1.0 (baseline) | — |

### Adding a New Regional Context

1. Create `contexts/[region].py` with the `MULTIPLIERS` dict (6 STEEEP × 3 temporal = 18 values)
2. Add detection keywords to `src/regional_context.py` in `_REGION_KEYWORDS`
3. Add the region to `context_map` in `get_multipliers()`
4. Optionally add `CONTEXT_NOTES` dict for report annotations

Example:
```python
# contexts/japan.py
MULTIPLIERS = {
    "Technological": {"Operational": 1.2, "Strategic": 1.3, "Civilizational": 1.1},
    ...
}
```

---

## Methodology Credits

Foresight Engine is inspired by established futures research methodologies:

| Methodology | Application |
|-------------|-------------|
| **IFTF Futures Cone** | Four scenario types: Probable, Plausible, Possible, Preferable |
| **STEEEP Framework** | Signal classification across 6 dimensions |
| **Futures Wheel** | Signal ripple effects in matrix cells |
| **Causal Layered Analysis (CLA)** | Operational → Strategic → Civilizational temporal layers |
| **Two Curves** | Tracking emerging vs incumbent trajectory signals |
| **Backcasting** | PREFERABLE scenario design from desired outcomes |
| **Cross-Impact Analysis** | STEEEP × Temporal matrix scoring |

Source: [Institute for the Future (IFTF)](https://www.iftf.org/)

---

## Running Tests

```bash
cd foresight-engine
pytest tests/ -v
```

All 7 test files, 174 tests.

---

## Author

**Santhosh Gandhi**
GitHub: [github.com/isanthoshgandhi](https://github.com/isanthoshgandhi)
Plugin: [github.com/isanthoshgandhi/foresight-engine](https://github.com/isanthoshgandhi/foresight-engine)
