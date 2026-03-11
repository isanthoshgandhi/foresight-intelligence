# Foresight Engine — MCP Server

**Author:** Santhosh Gandhi | [github.com/isanthoshgandhi/foresight-engine](https://github.com/isanthoshgandhi/foresight-engine)

---

## How It Works

The Foresight Engine has a strict division of labor between Claude and Python. Claude handles everything that requires judgment, language, and live information: collecting signals via web search, classifying signals into STEEEP categories, identifying historical analogues, writing scenario narratives, and assembling qualitative context. The MCP server handles everything that must be deterministic and reproducible: the 4-factor signal scoring formula, the 18-cell STEEEP×Temporal matrix population, probability normalization, confidence score arithmetic, and strategic stance derivation. By separating these responsibilities over the stdio transport, Claude can call precise arithmetic tools without ever generating numbers through reasoning, while the server never touches web search or narrative generation. This makes every score, probability, and confidence value auditable and identical across runs.

---

## Installation

```bash
pip install -r mcp_server/requirements.txt
```

**Requirements:** Python 3.10+, the `mcp` package (≥1.0.0), and all dependencies already present in the repo root (`src/` modules use only the Python standard library).

---

## Connect to Claude Desktop

### macOS

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

Replace `/ABSOLUTE/PATH/TO/foresight-engine` with the full path to your cloned repo.

### Windows

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "foresight-engine": {
      "command": "python",
      "args": ["C:\\ABSOLUTE\\PATH\\TO\\foresight-engine\\mcp_server\\server.py"],
      "env": {}
    }
  }
}
```

After editing either config file, **restart Claude Desktop completely** for the tools to appear.

---

## Connect to claude.ai Web

Use the `mcp-remote` bridge to expose the stdio server over HTTP so claude.ai can reach it.

### Step 1 — Install mcp-remote

```bash
npm install -g mcp-remote
```

### Step 2 — Start the bridge

```bash
cd /path/to/foresight-engine
mcp-remote python mcp_server/server.py --port 3100
```

The bridge starts a local HTTP server on port 3100 (change `--port` if there is a conflict).

### Step 3 — Register in claude.ai

1. Go to [claude.ai](https://claude.ai) → **Settings** → **Integrations** → **Add MCP Server**
2. Enter: `http://localhost:3100`
3. Save and start a new conversation — all 8 tools will appear in the tool list.

---

## Available Tools

| Tool Name | Pipeline Step | What It Does |
|---|---|---|
| `validate_input` | Step 1 — Validate Input | Runs 5 binary rules: entity reality, system existence, time horizon, signal availability, minimum specificity. Returns `{valid, rule_failed, failure_reason}`. |
| `score_signals` | Step 3 — Score Signals | Applies `recency × reliability × type × evidence` formula (capped at 1.0) to a batch of signals. Accepts optional regional multipliers. |
| `build_matrix` | Step 4 — Build Matrix | Populates the 6×3 STEEEP×Temporal grid from scored signals. Returns all 18 cell scores plus hot_zones (>0.5) and gap_zones (=0). |
| `get_regional_context` | Step 4b — Regional Context | Detects region from query keywords, returns full multiplier table and a context note explaining local structural factors. |
| `compute_probabilities` | Step 6a — Compute Probabilities | Normalizes raw PROBABLE/PLAUSIBLE/POSSIBLE scores to sum exactly to 100%. |
| `compute_confidence` | Step 6b — Compute Confidence | 3-factor weighted score: signal density (0–40 pts) + evidence balance (0–30 pts) + historical grounding (0–30 pts) → integer 0–100. |
| `compute_decision_guidance` | Step 7 — Decision Guidance | Derives recommended stance, low-regret move, and risk trigger deterministically from probabilities + confidence + matrix hot zones. |
| `format_report` | Step 8 — Format Report | Slots all content into the crisp Foresight Engine template. Supports `mode: "full"` (all 8 steps) or `mode: "quick"` (signal pulse + matrix only). |

---

## Troubleshooting

**"Module not found" on startup**
Run the server from the repo root, not from `mcp_server/`:
```bash
cd /path/to/foresight-engine
python mcp_server/server.py
```
The server inserts `src/` into `sys.path` relative to its own file location, so the working directory does not matter — but if you see import errors, check that `src/signal_scorer.py` exists at `../src/signal_scorer.py` relative to `server.py`.

**"Claude Desktop not showing tool"**
Config file changes require a full restart of Claude Desktop (Quit, not just close the window). On macOS use ⌘Q; on Windows close from the system tray. Verify the JSON is valid — a single missing comma will silently prevent all MCP servers from loading.

**"Port conflict" when using mcp-remote**
Change the port in the start command:
```bash
mcp-remote python mcp_server/server.py --port 3200
```
Then update the URL in claude.ai Settings to match (`http://localhost:3200`).
