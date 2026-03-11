"""
Transport: stdio. Claude handles web_search and reasoning. This server handles
deterministic arithmetic only. Never generate narrative or call web_search from
this server.

Foresight Engine MCP Server
============================
Wraps all deterministic Python modules from src/ as MCP tools.
Claude handles signal collection, reasoning, web search, narrative writing,
and historical analogue identification. This server handles arithmetic only:
scoring, matrix building, probability normalization, confidence computation,
decision guidance, and report formatting.

Each tool corresponds to one step of the 8-step Foresight Engine pipeline.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Sequence

# ── Ensure src/ is importable regardless of CWD ──────────────────────────────
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT / "src"))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
)

# ── Lazy imports from src/ (errors surfaced per-tool, not at startup) ─────────
def _import_src():
    """Import all src modules; returns dict of modules or raises ImportError."""
    import input_validator
    import signal_scorer
    import matrix_builder
    import regional_context
    import probability_calc
    import confidence_calc
    import decision_guidance
    import report_formatter
    return {
        "input_validator":  input_validator,
        "signal_scorer":    signal_scorer,
        "matrix_builder":   matrix_builder,
        "regional_context": regional_context,
        "probability_calc": probability_calc,
        "confidence_calc":  confidence_calc,
        "decision_guidance": decision_guidance,
        "report_formatter": report_formatter,
    }


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS: list[Tool] = [
    Tool(
        name="validate_input",
        description=(
            "Pipeline Step 1 — Validate Input. "
            "Runs 5 binary rules on the query to confirm it is real, specific, "
            "time-bounded, signal-researchable, and analytically useful. "
            "Calls input_validator.validate(query). "
            "Returns {valid, rule_failed, failure_reason, scope_note, proceed}. "
            "If valid=False, do not proceed with the pipeline."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The foresight question to validate, e.g. 'Will EVs dominate Indian cities by 2032?'"
                }
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="score_signals",
        description=(
            "Pipeline Step 3 — Score Signals. "
            "Applies the deterministic 4-factor formula to a batch of signals: "
            "score = recency_weight × reliability_weight × type_weight × evidence_multiplier (capped at 1.0). "
            "Calls signal_scorer.score_signal() for each signal in the batch, "
            "applying optional regional multipliers. "
            "Returns a list of scored signals with weights and final scores."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "signals": {
                    "type": "array",
                    "description": "Array of signal objects to score.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "content":         {"type": "string"},
                            "source_type":     {"type": "string", "enum": ["primary", "secondary", "opinion"]},
                            "signal_type":     {"type": "string", "enum": ["supporting", "opposing", "wildcard"]},
                            "steeep_category": {"type": "string"},
                            "temporal_layer":  {"type": "string"},
                            "recency_days":    {"type": "integer"},
                            "has_evidence":    {"type": "boolean"},
                            "source_url":      {"type": "string"},
                        },
                        "required": ["content"],
                    },
                },
                "multipliers": {
                    "type": "object",
                    "description": "Optional regional multipliers dict {steeep: {temporal: float}}. Pass {} for global baseline.",
                },
                "india_relevant": {
                    "type": "boolean",
                    "description": "Set true if query is India-specific (enables India multipliers).",
                    "default": False,
                },
            },
            "required": ["signals"],
        },
    ),
    Tool(
        name="build_matrix",
        description=(
            "Pipeline Step 4 — Build 6×3 STEEEP×Temporal Matrix. "
            "Populates all 18 cells of the matrix from scored signals. "
            "Calls matrix_builder.build_steeep_matrix(scored_signals). "
            "Returns the matrix with hot_zones (score >0.5), gap_zones (score=0), "
            "dominant zone, and signal counts."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "scored_signals": {
                    "type": "array",
                    "description": "Array of scored signal objects returned by score_signals tool.",
                    "items": {"type": "object"},
                },
            },
            "required": ["scored_signals"],
        },
    ),
    Tool(
        name="get_regional_context",
        description=(
            "Pipeline Step 4b — Get Regional Context. "
            "Detects the region from the query text, then returns the full "
            "multiplier table and a context note for that region. "
            "Calls regional_context.detect_region(query) → get_multipliers(region). "
            "Returns {region, multipliers, top_multipliers, context_note}."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The foresight question; region is auto-detected from keywords.",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="compute_probabilities",
        description=(
            "Pipeline Step 6a — Compute Probabilities. "
            "Normalizes raw scenario scores to sum to 100% across "
            "PROBABLE / PLAUSIBLE / POSSIBLE. PREFERABLE is value-based and excluded. "
            "Calls probability_calc.calculate_probabilities() with matrix and signals. "
            "Returns {probable_pct, plausible_pct, possible_pct} normalized to 100%."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "raw_scores": {
                    "type": "object",
                    "description": "Dict with keys probable, plausible, possible as raw float scores.",
                    "properties": {
                        "probable":  {"type": "number"},
                        "plausible": {"type": "number"},
                        "possible":  {"type": "number"},
                    },
                    "required": ["probable", "plausible", "possible"],
                },
                "signal_counts": {
                    "type": "object",
                    "description": "Dict with keys total, SUPPORTING, OPPOSING, WILDCARD.",
                    "properties": {
                        "total":      {"type": "integer"},
                        "SUPPORTING": {"type": "integer"},
                        "OPPOSING":   {"type": "integer"},
                        "WILDCARD":   {"type": "integer"},
                    },
                    "required": ["total"],
                },
            },
            "required": ["raw_scores"],
        },
    ),
    Tool(
        name="compute_confidence",
        description=(
            "Pipeline Step 6b — Compute Confidence Score. "
            "Computes a 0-100 confidence integer using signal density (0-40 pts), "
            "evidence balance (0-30 pts), and historical grounding (0-30 pts). "
            "Calls confidence_calc.calculate_confidence(). "
            "Returns {confidence_score: int} in range 0-100."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "scored_signals": {
                    "type": "array",
                    "description": "Array of scored signal objects from score_signals tool.",
                    "items": {"type": "object"},
                },
                "analogue_similarity": {
                    "type": "number",
                    "description": "Best historical analogue similarity score 0-100.",
                    "default": 0,
                },
            },
            "required": ["scored_signals"],
        },
    ),
    Tool(
        name="compute_decision_guidance",
        description=(
            "Pipeline Step 7 — Compute Decision Guidance. "
            "Deterministically derives recommended stance, low-regret move, "
            "and risk trigger from probabilities + confidence + matrix hot zones. "
            "Calls decision_guidance.compute_guidance(). "
            "Returns {recommended_stance, low_regret_move, risk_trigger, "
            "dominant_matrix_zone, confidence_in_guidance}."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "probabilities": {
                    "type": "object",
                    "description": "Dict with probable_pct, plausible_pct, possible_pct (sum to 100).",
                    "properties": {
                        "probable_pct":  {"type": "number"},
                        "plausible_pct": {"type": "number"},
                        "possible_pct":  {"type": "number"},
                    },
                    "required": ["probable_pct", "plausible_pct"],
                },
                "confidence": {
                    "type": "integer",
                    "description": "Confidence score 0-100 from compute_confidence tool.",
                },
                "hot_zones": {
                    "type": "array",
                    "description": "List of hot zone strings from build_matrix, e.g. ['Technological/Strategic'].",
                    "items": {"type": "string"},
                    "default": [],
                },
                "scored_signals": {
                    "type": "array",
                    "description": "Scored signals list for risk trigger computation.",
                    "items": {"type": "object"},
                    "default": [],
                },
            },
            "required": ["probabilities", "confidence"],
        },
    ),
    Tool(
        name="format_report",
        description=(
            "Pipeline Step 8 — Assemble and Format Report. "
            "Slots all Claude-written and computed content into the crisp Foresight Engine template. "
            "Calls report_formatter.format_from_dict(data) for full reports or "
            "a quick summary for quick mode. "
            "Returns the formatted plain-text report string."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "report_data": {
                    "type": "object",
                    "description": (
                        "Complete report data dict. Required keys: query, confidence, "
                        "signal_counts {total, SUPPORTING, OPPOSING, WILDCARD}, "
                        "matrix_summary {hot_zones, gap_zones, dominant_zone, net_direction}, "
                        "analogue {name, similarity, tipping_event, equivalent_exists}, "
                        "scenarios {probable, plausible, possible, preferable} each with "
                        "{narrative, proof, if_condition, but_condition}, "
                        "one_thing {insight, incident, watch, if_yes, if_no}, "
                        "guidance {recommended_stance, low_regret_move, risk_trigger}, "
                        "region, top_multipliers."
                    ),
                },
                "mode": {
                    "type": "string",
                    "description": "Report mode: 'full' (all 8 steps) or 'quick' (steps 1-4 + signal pulse only).",
                    "enum": ["full", "quick"],
                    "default": "full",
                },
            },
            "required": ["report_data"],
        },
    ),
]


# ── Tool handler helpers ──────────────────────────────────────────────────────

def _ok(data: Any) -> CallToolResult:
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(data, indent=2))],
        isError=False,
    )


def _err(message: str) -> CallToolResult:
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps({"error": message}, indent=2))],
        isError=True,
    )


# ── Individual tool implementations ──────────────────────────────────────────

def _handle_validate_input(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        iv = mods["input_validator"]
        query = args["query"]
        result = iv.validate(query)
        return _ok({
            "valid":          result.valid,
            "rule_failed":    result.rule_failed,
            "failure_reason": result.failure_reason,
            "scope_note":     result.scope_note,
            "proceed":        result.proceed,
        })
    except Exception as exc:
        return _err(
            f"validate_input failed: {exc}. "
            "Hint: ensure you are running from the repo root and src/ is importable."
        )


def _handle_score_signals(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        ss = mods["signal_scorer"]

        raw_signals = args.get("signals", [])
        multipliers = args.get("multipliers", {})
        india_relevant = bool(args.get("india_relevant", False))

        scored = []
        for s in raw_signals:
            signal_obj = ss.Signal(
                content=s.get("content", ""),
                source_type=s.get("source_type", "secondary"),
                signal_type=s.get("signal_type", "supporting"),
                steeep_category=s.get("steeep_category"),
                temporal_layer=s.get("temporal_layer"),
                recency_days=s.get("recency_days"),
                has_evidence=s.get("has_evidence", False),
                source_url=s.get("source_url"),
            )
            scored_signal = ss.score_signal(
                signal_obj,
                india_relevant=india_relevant,
                multipliers=multipliers if multipliers else None,
            )
            scored.append({
                "content":         scored_signal.signal.content,
                "source_type":     scored_signal.signal.source_type,
                "signal_type":     scored_signal.signal.signal_type,
                "steeep_category": scored_signal.steeep_category,
                "temporal_layer":  scored_signal.temporal_layer,
                "recency_weight":  scored_signal.recency_weight,
                "reliability_weight": scored_signal.reliability_weight,
                "type_weight":     scored_signal.type_weight,
                "evidence_weight": scored_signal.evidence_weight,
                "regional_multiplier": scored_signal.regional_multiplier,
                "final_score":     scored_signal.final_score,
            })
        return _ok({"scored_signals": scored, "count": len(scored)})
    except Exception as exc:
        return _err(
            f"score_signals failed: {exc}. "
            "Hint: each signal must have at least a 'content' field. "
            "Check signal source_type values: primary | secondary | opinion."
        )


def _handle_build_matrix(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        ss = mods["signal_scorer"]

        raw_scored = args.get("scored_signals", [])

        # Reconstruct ScoredSignal objects from dicts
        scored_objs = []
        for s in raw_scored:
            sig = ss.Signal(
                content=s.get("content", ""),
                source_type=s.get("source_type", "secondary"),
                signal_type=s.get("signal_type", "supporting"),
                steeep_category=s.get("steeep_category"),
                temporal_layer=s.get("temporal_layer"),
                recency_days=s.get("recency_days"),
                has_evidence=s.get("has_evidence", False),
                source_url=s.get("source_url"),
            )
            scored = ss.ScoredSignal(
                signal=sig,
                steeep_category=s.get("steeep_category", "Technological"),
                temporal_layer=s.get("temporal_layer", "Strategic"),
                recency_weight=s.get("recency_weight", 0.85),
                reliability_weight=s.get("reliability_weight", 0.75),
                type_weight=s.get("type_weight", 1.0),
                evidence_weight=s.get("evidence_weight", 1.0),
                regional_multiplier=s.get("regional_multiplier", 1.0),
                final_score=s.get("final_score", 0.5),
            )
            scored_objs.append(scored)

        matrix = ss.build_steeep_matrix(scored_objs)

        # Identify hot_zones and gap_zones
        hot_zones = []
        gap_zones = []
        for steeep in ss.STEEEP_CATEGORIES:
            for temporal in ss.TEMPORAL_LAYERS:
                cell = matrix.cells[steeep][temporal]
                cell_key = f"{steeep}/{temporal}"
                if cell.aggregate_score > 0.5:
                    hot_zones.append(cell_key)
                elif cell.aggregate_score == 0.0:
                    gap_zones.append(cell_key)

        return _ok({
            "signal_counts": matrix.signal_counts,
            "hot_zones":     hot_zones,
            "gap_zones":     gap_zones,
            "dominant_zone": hot_zones[0] if hot_zones else None,
            "net_direction": (
                "SUPPORTING" if matrix.signal_counts.get("SUPPORTING", 0)
                             > matrix.signal_counts.get("OPPOSING", 0)
                else "OPPOSING" if matrix.signal_counts.get("OPPOSING", 0)
                                > matrix.signal_counts.get("SUPPORTING", 0)
                else "NEUTRAL"
            ),
            "cells": {
                steeep: {
                    temporal: {
                        "aggregate_score": matrix.cells[steeep][temporal].aggregate_score,
                        "signal_count":    matrix.cells[steeep][temporal].signal_count,
                    }
                    for temporal in ss.TEMPORAL_LAYERS
                }
                for steeep in ss.STEEEP_CATEGORIES
            },
        })
    except Exception as exc:
        return _err(
            f"build_matrix failed: {exc}. "
            "Hint: pass the scored_signals array returned by score_signals. "
            "Each item must have steeep_category and temporal_layer."
        )


def _handle_get_regional_context(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        rc = mods["regional_context"]

        query = args["query"]
        region = rc.detect_region(query)
        multipliers = rc.get_multipliers(region)
        top_mults = rc.get_top_multipliers(region, n=3)

        # Context notes per region (replaces missing get_context_notes)
        _CONTEXT_NOTES = {
            "india": (
                "UPI/DPI infrastructure gives India asymmetric advantage in "
                "Technological/Operational signals. Mobile-first adoption and "
                "deep software talent pool amplify Technological signals. "
                "Political/Operational signals are dampened by regulatory fragmentation."
            ),
            "usa":   (
                "Deep capital markets and Silicon Valley ecosystem amplify "
                "Technological/Strategic signals. Political gridlock discounts "
                "Political/Operational signals relative to global baseline."
            ),
            "europe": (
                "Regulatory leadership (GDPR, EU AI Act) amplifies "
                "Environmental/Strategic signals. Economic/Civilizational "
                "signals are discounted by structural demographic headwinds."
            ),
            "china": (
                "State-directed capital amplifies Technological/Strategic signals "
                "significantly. Ethical/Operational signals are heavily discounted "
                "due to limited transparency and constrained civil discourse."
            ),
            "global": (
                "Global baseline: all multipliers = 1.0. No regional adjustment applied."
            ),
        }

        return _ok({
            "region":     region,
            "multipliers": multipliers,
            "top_multipliers": [
                {"steeep": s, "temporal": t, "value": v}
                for s, t, v in top_mults
            ],
            "context_note": _CONTEXT_NOTES.get(region, _CONTEXT_NOTES["global"]),
        })
    except Exception as exc:
        return _err(
            f"get_regional_context failed: {exc}. "
            "Hint: ensure the query string contains region keywords "
            "(e.g. 'india', 'usa', 'europe', 'china') or defaults to global."
        )


def _handle_compute_probabilities(args: dict) -> CallToolResult:
    try:
        raw_scores = args.get("raw_scores", {})
        prob_raw  = float(raw_scores.get("probable",  1.0))
        pla_raw   = float(raw_scores.get("plausible", 1.0))
        pos_raw   = float(raw_scores.get("possible",  1.0))

        total = prob_raw + pla_raw + pos_raw
        if total <= 0:
            total = 3.0
            prob_raw = pla_raw = pos_raw = 1.0

        prob_pct = round((prob_raw / total) * 100, 1)
        pla_pct  = round((pla_raw  / total) * 100, 1)
        pos_pct  = round(100.0 - prob_pct - pla_pct, 1)

        # signal counts for metadata
        sc = args.get("signal_counts", {})

        return _ok({
            "probable_pct":  prob_pct,
            "plausible_pct": pla_pct,
            "possible_pct":  pos_pct,
            "sum_check":     round(prob_pct + pla_pct + pos_pct, 1),
            "total_signals": sc.get("total", 0),
        })
    except Exception as exc:
        return _err(
            f"compute_probabilities failed: {exc}. "
            "Hint: pass raw_scores with keys probable, plausible, possible as floats."
        )


def _handle_compute_confidence(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        cc = mods["confidence_calc"]

        scored_signals = args.get("scored_signals", [])
        analogue_similarity = float(args.get("analogue_similarity", 0))

        total      = len(scored_signals)
        supporting = sum(1 for s in scored_signals if s.get("signal_type") == "supporting")
        opposing   = sum(1 for s in scored_signals if s.get("signal_type") == "opposing")

        signal_counts = {
            "total":      total,
            "SUPPORTING": supporting,
            "OPPOSING":   opposing,
        }

        # Build a minimal Matrix-compatible object using signal_scorer
        ss = mods["signal_scorer"]
        Matrix = ss.Matrix
        dummy_matrix = Matrix()
        dummy_matrix.signal_counts = signal_counts

        score = cc.calculate_confidence(
            matrix=dummy_matrix,
            signal_counts=signal_counts,
            analogue_similarity=analogue_similarity,
        )

        return _ok({
            "confidence_score": score,
            "signal_density_input": total,
            "evidence_balance_input": {"supporting": supporting, "opposing": opposing},
            "analogue_similarity_input": analogue_similarity,
        })
    except Exception as exc:
        return _err(
            f"compute_confidence failed: {exc}. "
            "Hint: pass scored_signals (output of score_signals tool) and "
            "analogue_similarity as a float 0-100."
        )


def _handle_compute_decision_guidance(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        dg = mods["decision_guidance"]

        probabilities     = args.get("probabilities", {})
        confidence        = int(args.get("confidence", 50))
        hot_zones         = args.get("hot_zones", [])
        scored_signals    = args.get("scored_signals", [])

        hottest_cell  = hot_zones[0] if hot_zones else "Technological/Strategic"
        net_direction = "NEUTRAL"

        if scored_signals:
            supporting = sum(1 for s in scored_signals if s.get("signal_type") == "supporting")
            opposing   = sum(1 for s in scored_signals if s.get("signal_type") == "opposing")
            if supporting > opposing:
                net_direction = "SUPPORTING"
            elif opposing > supporting:
                net_direction = "OPPOSING"

        matrix_summary = {
            "hottest_cell":  hottest_cell,
            "net_direction": net_direction,
        }

        guidance = dg.compute_guidance(
            probabilities=probabilities,
            matrix=matrix_summary,
            scored_signals=scored_signals,
            confidence_score=confidence,
        )
        return _ok(guidance)
    except Exception as exc:
        return _err(
            f"compute_decision_guidance failed: {exc}. "
            "Hint: pass probabilities dict (probable_pct, plausible_pct, possible_pct), "
            "confidence integer 0-100, and hot_zones list from build_matrix."
        )


def _handle_format_report(args: dict) -> CallToolResult:
    try:
        mods = _import_src()
        rf = mods["report_formatter"]

        report_data = args.get("report_data", {})
        mode = args.get("mode", "full")

        if mode == "quick":
            # Quick mode: format just signal pulse + matrix summary
            query        = report_data.get("query", "")
            sc           = report_data.get("signal_counts", {"total": 0, "SUPPORTING": 0, "OPPOSING": 0, "WILDCARD": 0})
            matrix_info  = report_data.get("matrix_summary", {})
            confidence   = report_data.get("confidence", 0)
            region       = report_data.get("region", "global")
            top_mults    = report_data.get("top_multipliers", [])

            sup_n = sc.get("SUPPORTING", 0)
            opp_n = sc.get("OPPOSING", 0)
            wld_n = sc.get("WILDCARD", 0)
            tot_n = sc.get("total", 0)
            max_n = max(sup_n, opp_n, 1)

            def _bar(n, m): return "█" * int(n / m * 20) + "░" * (20 - int(n / m * 20))

            divider = "━" * 31
            lines = [
                divider,
                "FORESIGHT ENGINE (QUICK MODE)",
                query,
                f"Confidence: {confidence}/100 | Signals: {tot_n}",
                divider,
                "",
                "SIGNAL PULSE",
                f"Supporting {sup_n} [{_bar(sup_n, max_n)}] | Opposing {opp_n} [{_bar(opp_n, max_n)}] | Wild {wld_n}",
                f"Net: {matrix_info.get('net_direction', 'NEUTRAL')}",
                f"Hot zone: {', '.join(matrix_info.get('hot_zones', ['—'])[:2])}",
                f"Gap: {', '.join(matrix_info.get('gap_zones', ['—'])[:2])}",
                "",
                f"[REGIONAL LENS — {region.upper()}]",
            ]
            for m in top_mults[:2]:
                if isinstance(m, dict):
                    lines.append(f"  {m.get('steeep','')}/{m.get('temporal','')} ({m.get('value',1.0):.2f}x)")
            lines.append(divider)
            return _ok({"report_text": "\n".join(lines), "mode": "quick"})

        # Full mode — delegate to format_from_dict
        report_text = rf.format_from_dict(report_data)
        return _ok({"report_text": report_text, "mode": "full"})

    except Exception as exc:
        return _err(
            f"format_report failed: {exc}. "
            "Hint: report_data must include query, signal_counts, confidence, "
            "scenarios (probable/plausible/possible/preferable), one_thing, and guidance. "
            "Use mode='quick' for a signal-pulse-only output."
        )


# ── MCP Server setup ──────────────────────────────────────────────────────────

app = Server("foresight-engine")


@app.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    dispatch = {
        "validate_input":          _handle_validate_input,
        "score_signals":           _handle_score_signals,
        "build_matrix":            _handle_build_matrix,
        "get_regional_context":    _handle_get_regional_context,
        "compute_probabilities":   _handle_compute_probabilities,
        "compute_confidence":      _handle_compute_confidence,
        "compute_decision_guidance": _handle_compute_decision_guidance,
        "format_report":           _handle_format_report,
    }
    handler = dispatch.get(name)
    if handler is None:
        result = _err(f"Unknown tool: {name}. Available: {list(dispatch.keys())}")
    else:
        result = handler(arguments)
    return result.content


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
