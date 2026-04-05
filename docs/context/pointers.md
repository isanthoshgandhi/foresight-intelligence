# Foresight Engine — Session Pointers

> Read this file FIRST on every session.
> Pick your domain. Load ONLY those files.

## QUICK RESUME
Last session: 2026-03-22 (approx)
Where we left off: v2.1.0 — both modes functional. Soft predict (Claude skill) + Hard predict (Python agent, deterministic scoring).
Next action: Check `docs/context/main.md` for open questions and next improvements.

---

## Domain: soft-predict
*Claude-native skill — instant foresight, works on claude.ai and Claude Code*

Load:
1. `docs/context/main.md` — engine design, methodology, open questions

Skip: agents/ directory

---

## Domain: hard-predict
*Deterministic Python agent — 12-step, auditable, JSON output*

Load:
1. `docs/context/main.md` — engine design, scoring formula, output format

Skim if needed:
- `agents/hard-predict-future/` — agent source

---

## What NOT to load
| File | Why skip |
|---|---|
| `README.md` | Full overview — read only for user-facing docs update |
| `agents/` | Agent source — load only when modifying specific step |
| `skills/` | Skill source — load only when modifying soft predict |
