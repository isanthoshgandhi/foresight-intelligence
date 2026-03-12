# Foresight Engine — for Claude Desktop (MCP Server)

> **This version is built for [Claude Desktop](https://claude.ai/download) via MCP.**
> Looking for a different platform? → [Claude.ai Skill](https://github.com/isanthoshgandhi/foresight-engine-skill) · [Claude Code Plugin](https://github.com/isanthoshgandhi/foresight-engine-plugin)

**Author:** Santhosh Gandhi

AI-powered strategic foresight engine using IFTF methodology. Claude handles web search, reasoning, and narratives. This MCP server handles all deterministic arithmetic: signal scoring, STEEEP matrix, probability normalization, confidence calculation, and report formatting. Every number is computed in Python — never hallucinated.

---

## What This Does

Given a forecasting question like *"Will EVs dominate Indian cities by 2032?"*, the engine runs an 8-step pipeline:

1. **Validate** — 5 binary rules confirm the query is specific, real, and signal-researchable
2. **Collect signals** — Claude searches the web for 18+ real-world signals
3. **Score signals** — deterministic 4-factor formula: `recency × reliability × type × evidence`
4. **Build STEEEP matrix** — 18-cell grid (6 STEEEP categories × 3 temporal layers)
5. **Regional context** — multipliers for India, USA, Europe, China
6. **Compute probabilities** — normalized to sum exactly to 100%
7. **Decision guidance** — stance, low-regret move, risk trigger
8. **Format report** — crisp four-scenario intelligence report

---

## Requirements

- Python 3.10+
- Claude Desktop (macOS or Windows)
- `mcp >= 1.0.0`

---

## Installation

**Step 1 — Clone and install dependencies**

```bash
git clone https://github.com/isanthoshgandhi/foresight-engine.git
cd foresight-engine
pip install -r mcp_server/requirements.txt
```

**Step 2 — Connect to Claude Desktop**

**macOS** — Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "foresight-engine": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/foresight-engine/mcp_server/server.py"]
    }
  }
}
```

**Windows** — Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "foresight-engine": {
      "command": "python",
      "args": ["C:\ABSOLUTE\PATH\TO\foresight-engine\mcp_server\server.py"]
    }
  }
}
```

Replace the path with the actual path on your machine.

**Step 3 — Restart Claude Desktop completely** (Quit, not just close the window).

The 8 foresight tools will appear in Claude Desktop's tool list.

---

## Available MCP Tools

| Tool | Pipeline Step | Purpose |
|---|---|---|
| `validate_input` | Step 1 | Validates query against 5 binary rules |
| `score_signals` | Step 3 | Scores signals with 4-factor formula |
| `build_matrix` | Step 4 | Builds 18-cell STEEEP×Temporal matrix |
| `get_regional_context` | Step 4b | Returns regional multipliers and context |
| `compute_probabilities` | Step 6a | Normalizes scenario probabilities to 100% |
| `compute_confidence` | Step 6b | Computes 0–100 confidence score |
| `compute_decision_guidance` | Step 7 | Derives stance, low-regret move, risk trigger |
| `format_report` | Step 8 | Assembles final intelligence report |

---

## Usage

Once connected, ask Claude Desktop:

```
Run a foresight analysis on: Will generative AI replace junior software engineers in India by 2028?
```

Claude will automatically use the MCP tools for all arithmetic steps and handle web search and reasoning natively.

---

## How It Works

Claude and the MCP server have a strict division of labor:

- **Claude handles:** web search, signal classification, historical analogues, scenario narratives, qualitative reasoning
- **MCP server handles:** all numbers — scoring formulas, matrix population, probability normalization, confidence arithmetic

This separation means every score, probability, and confidence value is deterministic and auditable across runs.

---

## Troubleshooting

**Tools not appearing in Claude Desktop**
Full restart required (Quit, not just close). Verify your JSON config has no syntax errors — a single missing comma silently prevents all MCP servers from loading.

**"Module not found" errors**
The server auto-resolves `src/` relative to its own path. If you see import errors, confirm `src/signal_scorer.py` exists at `../src/signal_scorer.py` relative to `mcp_server/server.py`.

---

## Other Versions

| Platform | Repo |
|---|---|
| Claude Desktop (this) | [foresight-engine](https://github.com/isanthoshgandhi/foresight-engine) |
| Claude.ai (web skill) | [foresight-engine-skill](https://github.com/isanthoshgandhi/foresight-engine-skill) |
| Claude Code (CLI plugin) | [foresight-engine-plugin](https://github.com/isanthoshgandhi/foresight-engine-plugin) |

---

## License

MIT
