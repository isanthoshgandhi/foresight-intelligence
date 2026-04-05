# Foresight Engine — Context

> Updated: 2026-03-22
> READ THIS FIRST

---

## RESUME FROM HERE
Last session: 2026-03-22 (approx)
What was done: v2.1.0 — both modes complete, year is optional (engine infers horizon)
Current state: Fully functional. Soft predict + Hard predict both working.
Open bugs: None known
Next action: Improve scenario quality or add new example prompts to README

---

## What This Is
Strategic foresight engine using IFTF methodology.
- **Soft Predict:** Claude-native skill, instant, works on claude.ai. No Python needed.
- **Hard Predict:** Deterministic 12-step Python agent. Identical output every run. Auditable JSON.

## Key Design Decisions
- Year is optional — engine infers time horizon from question
- Hard predict uses structural drivers + cross-impact analysis + IFTF backcasting
- Four-scenario reports with VERDICT
- Hard predict produces JSON audit trail per step

## Structure
```
agents/
  hard-predict-future/    -- 12-step deterministic agent
  soft-predict-future/    -- Claude skill
  foresight-analyst.md    -- analyst agent
skills/                   -- (if any skill variants)
```

## Key Files
- `README.md` — full methodology + example prompts
- `agents/hard-predict-future/` — Python agent source
- `agents/soft-predict-future/` — skill source

## Open Questions
- Add confidence intervals to hard predict output?
- Publish as standalone Claude plugin?
