# Foresight Engine — AI Strategic Foresight Plugin for Claude

> **Four-scenario intelligence reports backed by live signals, historical analogues, and deterministic probability scoring.**
> Built for VC due diligence, startup strategy, and market intelligence.

[![Version](https://img.shields.io/badge/version-1.2.0-blue)](https://github.com/isanthoshgandhi/foresight-engine)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-174%20passing-brightgreen)](tests/)
[![Claude Plugin](https://img.shields.io/badge/Claude-Plugin-orange)](https://claude.ai)

**Author:** Santhosh Gandhi | [GitHub](https://github.com/isanthoshgandhi) | [isanthoshgandhi@gmail.com](mailto:isanthoshgandhi@gmail.com)

---

## Quick Start

**Claude Code CLI:**
```
/plugin marketplace add isanthoshgandhi/foresight-engine
/plugin install foresight-engine@isanthoshgandhi
/foresight-engine:analyze "Will India produce a $50B SaaS company by 2035?"
```

**Cowork (personal plugin):** Download [`foresight-engine.plugin`](https://github.com/isanthoshgandhi/foresight-engine/releases) → Cowork → Plugins → Add Personal Plugin → Upload

**Claude.ai (no install):** Paste [`SKILL.md`](SKILL.md) into Settings → Custom Skills

---

## What It Does

Foresight Engine is a strategic intelligence plugin for Claude Code. Give it any real-world question about the future — a sector, a technology, a geopolitical shift — and it produces a structured four-scenario analysis backed by live signals, historical analogues, and deterministic probability scoring.

It augments Claude's native capabilities with a structured methodology layer inspired by IFTF foresight practices (Futures Cone, STEEEP, Cross-Impact Analysis, Backcasting). The result is a crisp intelligence report you can act on.

**Best for:**
- VC deal screening and sector due diligence
- Startup market timing and strategy validation
- Policy and geopolitical scenario planning
- Product market fit and competitive landscape analysis

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

### Option 1 — Claude Code CLI (Recommended)

```bash
# Add the plugin marketplace
/plugin marketplace add isanthoshgandhi/foresight-engine

# Install the plugin
/plugin install foresight-engine@isanthoshgandhi

# Verify
/plugin list
```

**Requirements:** Claude Code CLI, Python 3.10+

### Option 2 — Cowork Personal Plugin

Download the latest `foresight-engine.plugin` from [Releases](https://github.com/isanthoshgandhi/foresight-engine/releases), then:
1. Open Cowork → Plugins → Add Personal Plugin
2. Upload `foresight-engine.plugin`

### Option 3 — Claude.ai Personal Skill (No install)

1. Open [claude.ai](https://claude.ai) → **Settings** → **Custom Skills**
2. Upload or paste the contents of [`SKILL.md`](SKILL.md)
3. Save — Claude will follow the full 8-step methodology for any foresight query

> **Note:** The Skill version uses Claude's approximation for arithmetic. For VC-grade reproducible outputs, use Option 1 or Option 2.

---

## Three-Environment Support

| Environment | Entry Point | Arithmetic | When to Use |
|---|---|---|---|
| **Claude Code CLI** (plugin) | `commands/` + `src/` | Python (exact) | Full reproducibility; VC/investment memos |
| **Claude.ai via MCP Server** | `mcp_server/server.py` | Python (exact) | Claude Desktop with live Python over stdio |
| **Claude.ai Personal Skill** | `SKILL.md` | LLM (approximate ±3%) | Exploratory analysis; no local setup |

### MCP Server Setup

```bash
pip install -r mcp_server/requirements.txt
```

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "foresight-engine": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/foresight-engine/mcp_server/server.py"],
      "env": {}
    }
  }
}
```

Restart Claude Desktop after editing. See [`mcp_server/README.md`](mcp_server/README.md) for claude.ai web bridge instructions.

---

## Commands

### `/foresight-engine:analyze` — Full 8-step pipeline

```
/foresight-engine:analyze "Will EVs dominate global cities by 2035?"
/foresight-engine:analyze "Will India produce a $50B SaaS company by 2035?"
/foresight-engine:analyze "Will China surpass the US in AI by 2035?"
```

### `/foresight-engine:quick` — Signal pulse only (fast, ~60 seconds)

```
/foresight-engine:quick "Will Indian fintech dominate SEA by 2030?"
/foresight-engine:quick "Is quantum computing a near-term threat to encryption?"
```

Runs Steps 1–4 + 6 only. No scenario writing. Returns probability distribution and signal pulse.

### `/foresight-engine:region` — Full pipeline with expanded regional lens

```
/foresight-engine:region "Will Indian B2B SaaS produce a $50B company by 2035?"
/foresight-engine:region "Will European green tech lead global markets by 2030?"
```

### `/foresight-engine:india` — Full pipeline with India-specific lens

```
/foresight-engine:india "Will UPI replace cash in Tier 3 Indian cities by 2030?"
/foresight-engine:india "Will India's EV sector produce a global OEM by 2035?"
```

Adds extra searches: RBI, SEBI, NITI Aayog, UPI/DPI ecosystem, India vs China comparison.

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

```python
# contexts/japan.py
MULTIPLIERS = {
    "Technological": {"Operational": 1.2, "Strategic": 1.3, "Civilizational": 1.1},
    ...
}
```

---

## Methodology

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

7 test files, 174 tests covering all Python modules.

---

## Contributing

1. Fork the repo and create a feature branch
2. Follow the two-layer rule: Python for arithmetic, Claude for reasoning
3. Add tests for any new Python module logic
4. Submit a PR with a clear description

To add a new region: see [Adding a New Regional Context](#adding-a-new-regional-context) above.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Santhosh Gandhi**
GitHub: [github.com/isanthoshgandhi](https://github.com/isanthoshgandhi)
Email: [isanthoshgandhi@gmail.com](mailto:isanthoshgandhi@gmail.com)
Plugin: [github.com/isanthoshgandhi/foresight-engine](https://github.com/isanthoshgandhi/foresight-engine)
