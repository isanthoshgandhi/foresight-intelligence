# Foresight Engine

> AI-powered strategic foresight using IFTF methodology. Four-scenario intelligence reports backed by live signals, historical analogues, and deterministic probability scoring.
>
> **Author:** Santhosh Gandhi

---

## Which version should I install?

| I use... | Install this |
|---|---|
| [claude.ai](https://claude.ai) (web) | [Skill — one click install](#install-on-claudeai) |
| Claude Code (terminal) | [Plugin — two command install](#install-on-claude-code) |

---

## Install on claude.ai

1. Go to [claude.ai](https://claude.ai) → **Profile** → **Skills**
2. Click **Add Skill from GitHub**
3. Enter: `https://github.com/isanthoshgandhi/foresight-engine`
4. Done — start a new conversation and ask:

```
Foresight analysis: Will generative AI replace junior software engineers in India by 2028?
```

---

## Install on Claude Code

```bash
# Step 1 — Add the marketplace (one-time setup)
claude plugin marketplace add https://github.com/isanthoshgandhi/foresight-engine

# Step 2 — Install the plugin
claude plugin install foresight-engine
```

Then use the commands:

```
/foresight-engine:analyze Will EVs dominate Indian cities by 2032?
/foresight-engine:quick   Will crypto replace banks by 2030?
/foresight-engine:region  Will US tech regulation fragment the internet by 2030?
/foresight-engine:india   Will UPI become Southeast Asia's payment standard by 2028?
```

---

## Commands (Claude Code)

| Command | What it does |
|---|---|
| `/foresight-engine:analyze` | Get a full strategic forecast — 4 scenarios, probability scores, and a clear action recommendation. *e.g. Will EVs dominate Indian cities by 2032?* |
| `/foresight-engine:quick` | Fast read on any future question in under a minute — see how evidence stacks up with a quick probability estimate. *e.g. Will remote work become permanent by 2027?* |
| `/foresight-engine:region` | Full forecast with deep regional context for India, USA, Europe or China. *e.g. Will US tech regulation fragment the internet by 2030?* |
| `/foresight-engine:india` | Full forecast built specifically for India — extra research on Indian policy, UPI/DPI, and startup ecosystem. *e.g. Will UPI become Southeast Asia's payment standard by 2028?* |

---

## What you get

A four-scenario intelligence report:

- **PROBABLE** — Most likely path (>=50%)
- **PLAUSIBLE** — Credible alternative (~30%)
- **POSSIBLE** — Low-probability but real (~15%)
- **PREFERABLE** — Best-case if conditions align (~5%)

Each scenario includes: key drivers, supporting evidence, historical analogues, probability score, and decision guidance.

---

## How it works

The pipeline runs 8 steps:

1. **Validate** — confirms the query is specific, real, and signal-researchable
2. **Collect signals** — web search for 18+ real-world signals
3. **Score signals** — 4-factor formula: recency x reliability x type x evidence
4. **Build STEEEP matrix** — 18-cell grid across 6 categories x 3 time horizons
5. **Regional context** — multipliers for India, USA, Europe, China
6. **Compute probabilities** — normalized to sum exactly to 100%
7. **Decision guidance** — stance, low-regret move, risk trigger
8. **Format report** — crisp four-scenario output

---

## License

MIT
