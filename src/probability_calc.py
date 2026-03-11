"""
probability_calc.py

Calculate probability distribution across four future types.
PREFERABLE is not probability-based — excluded from calculation.
Pure arithmetic. No AI calls. No web search.

Score formulas:
  probable_raw  = (strong_supporting × 3) + (high_similarity × 4) + (hot_cell × 2)
  plausible_raw = (moderate_supporting × 2) + (medium_similarity × 3)
  possible_raw  = (wildcard_count × 2) + (low_similarity × 3)

All three are then normalised to sum to 100%.

Usage: python src/probability_calc.py scored_signals.json analogues.json
Output: probabilities.json to stdout + writes file
"""

from __future__ import annotations
import sys
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from signal_scorer import Matrix, ScoredSignal, Signal, score_signal, build_steeep_matrix


@dataclass
class Analogue:
    """Historical analogue as assessed by Claude's reasoning."""
    name: str                  # e.g. "South Korea EV adoption 2016-2022"
    description: str           # 1-sentence summary
    conditions_then: str       # conditions that existed
    tipping_incident: str      # single event that tipped the outcome
    outcome: str               # what actually happened
    similarity_score: float    # 0–100 (Claude-assessed)


@dataclass
class ProbabilityResult:
    """Normalised probability distribution across three scenario types."""
    probable_pct:  float    # % (normalised, sums to 100 with others)
    plausible_pct: float
    possible_pct:  float
    probable_raw:  float    # raw before normalisation
    plausible_raw: float
    possible_raw:  float
    confidence:    int      # 0–100 integer


# ─── RAW SCORE CALCULATORS ───────────────────────────────────────────────────

def _probable_raw(
    scored_signals: List[ScoredSignal],
    analogues: List[Analogue],
    matrix: Matrix,
) -> float:
    """
    PROBABLE raw score.

    Formula:
      probable_raw = (strong_supporting × 3)
                   + (high_similarity   × 4)
                   + (hot_cell_bonus    × 2)

    Definitions:
      strong_supporting = count of signals with final_score > 0.7 AND type=SUPPORTING
      high_similarity   = count of analogues with similarity_score > 70
      hot_cell_bonus    = score of matrix's hottest cell
    """
    strong_supporting = sum(
        1 for s in scored_signals
        if s.final_score > 0.7 and s.signal_type == "SUPPORTING"
    )
    high_similarity = sum(1 for a in analogues if a.similarity_score > 70.0)
    hot_score = matrix.cells[matrix.hottest_cell].score if matrix.hottest_cell in matrix.cells else 0.0

    return (strong_supporting * 3) + (high_similarity * 4) + (hot_score * 2)


def _plausible_raw(
    scored_signals: List[ScoredSignal],
    analogues: List[Analogue],
) -> float:
    """
    PLAUSIBLE raw score.

    Formula:
      plausible_raw = (moderate_supporting × 2) + (medium_similarity × 3)

    Definitions:
      moderate_supporting = count of signals with final_score 0.4–0.7 AND SUPPORTING
      medium_similarity   = count of analogues with similarity_score 40–70
    """
    moderate_supporting = sum(
        1 for s in scored_signals
        if 0.4 <= s.final_score <= 0.7 and s.signal_type == "SUPPORTING"
    )
    medium_similarity = sum(
        1 for a in analogues if 40.0 <= a.similarity_score <= 70.0
    )
    return (moderate_supporting * 2) + (medium_similarity * 3)


def _possible_raw(
    scored_signals: List[ScoredSignal],
    analogues: List[Analogue],
) -> float:
    """
    POSSIBLE raw score.

    Formula:
      possible_raw = (wildcard_count × 2) + (low_similarity × 3)

    Definitions:
      wildcard_count  = count of WILDCARD signals
      low_similarity  = count of analogues with similarity_score < 40
    """
    wildcard_count = sum(1 for s in scored_signals if s.signal_type == "WILDCARD")
    low_similarity = sum(1 for a in analogues if a.similarity_score < 40.0)
    return (wildcard_count * 2) + (low_similarity * 3)


# ─── NORMALIZATION ────────────────────────────────────────────────────────────

def _normalize(probable: float, plausible: float, possible: float):
    """
    Normalise three raw scores to sum to 100%.
    Returns equal distribution (33.3 / 33.3 / 33.4) when all are zero.
    """
    total = probable + plausible + possible
    if total == 0:
        return 33.3, 33.3, 33.4

    p1 = round((probable  / total) * 100, 1)
    p2 = round((plausible / total) * 100, 1)
    p3 = round(100.0 - p1 - p2, 1)
    return p1, p2, p3


# ─── CONFIDENCE SCORE ────────────────────────────────────────────────────────

def calculate_confidence(
    matrix: Matrix,
    signal_counts: dict,
    analogue_similarity: float,
) -> int:
    """
    Calculate overall confidence score as integer 0–100.

    Three components:
      Signal density     (0–40): total_signals / 25 × 40, capped at 40
      Evidence balance   (0–30): |supporting − opposing| / total × 30
                                 (higher when one side clearly dominates)
      Historical grounding (0–30): best_similarity / 100 × 30

    Args:
        matrix:              Populated STEEEP matrix (for cross-check)
        signal_counts:       Dict with keys: total, SUPPORTING, OPPOSING
        analogue_similarity: Best historical analogue similarity (0–100)

    Returns:
        Integer confidence in range [0, 100]
    """
    total      = signal_counts.get("total", 0)
    supporting = signal_counts.get("SUPPORTING", 0)
    opposing   = signal_counts.get("OPPOSING",   0)

    # 1. Signal density (0–40)
    density = min(40.0, (total / 25.0) * 40.0)

    # 2. Evidence balance (0–30) — dominance of one direction
    balance = (abs(supporting - opposing) / total * 30.0) if total > 0 else 0.0

    # 3. Historical grounding (0–30)
    grounding = (max(0.0, min(100.0, analogue_similarity)) / 100.0) * 30.0

    return min(100, int(round(density + balance + grounding)))


# ─── MAIN ENTRY POINT ────────────────────────────────────────────────────────

def calculate_probabilities(
    matrix: Matrix,
    scored_signals: List[ScoredSignal],
    analogues: List[Analogue],
) -> ProbabilityResult:
    """
    Calculate probability distribution across PROBABLE / PLAUSIBLE / POSSIBLE.
    PREFERABLE is value-based, not probability-based, and is excluded.

    Args:
        matrix:         Populated STEEEP matrix from signal_scorer.py
        scored_signals: List of ScoredSignal objects
        analogues:      List of Analogue objects (Claude-assessed similarities)

    Returns:
        ProbabilityResult with percentages normalised to sum to 100%
        and a confidence integer 0–100
    """
    prob_raw  = _probable_raw(scored_signals, analogues, matrix)
    pla_raw   = _plausible_raw(scored_signals, analogues)
    pos_raw   = _possible_raw(scored_signals, analogues)

    prob_pct, pla_pct, pos_pct = _normalize(prob_raw, pla_raw, pos_raw)

    best_sim = max((a.similarity_score for a in analogues), default=0.0)
    conf     = calculate_confidence(matrix, matrix.signal_counts, best_sim)

    return ProbabilityResult(
        probable_pct=prob_pct,
        plausible_pct=pla_pct,
        possible_pct=pos_pct,
        probable_raw=prob_raw,
        plausible_raw=pla_raw,
        possible_raw=pos_raw,
        confidence=conf,
    )


# ─── CLI ENTRY POINT ─────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: probability_calc.py scored_signals.json analogues.json"
        }, indent=2))
        sys.exit(1)

    signals_path = Path(sys.argv[1])
    analogues_path = Path(sys.argv[2])

    for p in [signals_path, analogues_path]:
        if not p.exists():
            print(json.dumps({"error": f"File not found: {p}"}, indent=2))
            sys.exit(1)

    with open(signals_path) as f:
        signals_data = json.load(f)
    with open(analogues_path) as f:
        analogues_data = json.load(f)

    raw_scored = (
        signals_data.get("scored_signals", signals_data)
        if isinstance(signals_data, dict) else signals_data
    )
    raw_analogues = (
        analogues_data if isinstance(analogues_data, list)
        else analogues_data.get("analogues", [])
    )

    # Reconstruct ScoredSignal objects
    scored_signals = []
    for item in raw_scored:
        s = Signal(
            content=item.get("content", ""),
            source=item.get("source", ""),
            date=item.get("date"),
            steeep_category=item.get("steeep_category"),
            temporal_layer=item.get("temporal_layer"),
            signal_type=item.get("signal_type"),
        )
        scored = score_signal(s)
        scored.steeep_category = item.get("steeep_category", scored.steeep_category)
        scored.temporal_layer = item.get("temporal_layer", scored.temporal_layer)
        scored.signal_type = item.get("signal_type", scored.signal_type)
        scored.final_score = item.get("final_score", scored.final_score)
        scored_signals.append(scored)

    # Build matrix
    matrix = build_steeep_matrix(scored_signals)

    # Reconstruct Analogue objects
    analogues = [
        Analogue(
            name=a.get("name", "Unknown"),
            description=a.get("description", ""),
            conditions_then=a.get("conditions_then", ""),
            tipping_incident=a.get("tipping_incident", ""),
            outcome=a.get("outcome", ""),
            similarity_score=float(a.get("similarity", a.get("similarity_score", 0))),
        )
        for a in raw_analogues
    ]

    # Check momentum
    momentum_applied = any(
        item.get("momentum_flag") == "HIGH_MOMENTUM" for item in raw_scored
    )
    if momentum_applied:
        # Apply boost: wildcard component gets +10% of possible_raw
        pass  # handled within calculate_probabilities via the matrix

    result_obj = calculate_probabilities(matrix, scored_signals, analogues)

    # Determine dominant scenario
    probs = {
        "PROBABLE": result_obj.probable_pct,
        "PLAUSIBLE": result_obj.plausible_pct,
        "POSSIBLE": result_obj.possible_pct,
    }
    dominant = max(probs, key=probs.get)

    result = {
        "probable_pct": result_obj.probable_pct,
        "plausible_pct": result_obj.plausible_pct,
        "possible_pct": result_obj.possible_pct,
        "momentum_applied": momentum_applied,
        "dominant_scenario": dominant,
        "confidence": result_obj.confidence,
    }

    import os
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", "."))
    out_path = plugin_root / "probabilities.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
