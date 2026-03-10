"""
india_context.py

India-specific multipliers for signal scoring.
Applied by signal_scorer.py when query is India-relevant.
Pure arithmetic — no AI calls, no web search.

Multiplier guide:
  > 1.0  India has asymmetric advantage or exposure in this cell
  < 1.0  India has structural disadvantage or dampening factor
  = 1.0  Neutral — India tracks global baseline
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from signal_scorer import ScoredSignal


# ─── MULTIPLIER TABLE (6 × 3) ─────────────────────────────────────────────────
MULTIPLIERS = {
    "Social": {
        "Operational":    1.1,   # rising aspiration, urban-rural gap
        "Strategic":      1.3,   # demographic dividend, rising middle class
        "Civilizational": 1.2,   # language/identity diversity, cultural depth
    },
    "Technological": {
        "Operational":    1.4,   # UPI/DPI advantage, mobile-first adoption
        "Strategic":      1.3,   # software talent depth, IT services scale
        "Civilizational": 0.9,   # hardware gap, semiconductor dependency
    },
    "Economic": {
        "Operational":    1.0,   # neutral — tracks global cycles
        "Strategic":      1.3,   # large domestic market, manufacturing push
        "Civilizational": 0.9,   # cost arbitrage compressing, commodity import
    },
    "Environmental": {
        "Operational":    0.9,   # policy lag, enforcement gaps
        "Strategic":      1.0,   # neutral — renewable push vs coal dependency
        "Civilizational": 1.1,   # climate vulnerability high (monsoon/coastal/heat)
    },
    "Ethical": {
        "Operational":    0.9,   # regulatory unpredictability, enforcement gaps
        "Strategic":      1.0,   # neutral — digital rights framework emerging
        "Civilizational": 1.0,   # neutral — complex multi-stakeholder landscape
    },
    "Political": {
        "Operational":    0.85,  # regulatory unpredictability, state-federal friction
        "Strategic":      1.2,   # PLI/industrial policy tailwind, reform momentum
        "Civilizational": 1.15,  # US-China geopolitical positioning advantage
    },
}

# Keywords that identify a query as India-relevant
INDIA_KEYWORDS = [
    "india", "indian", "bharatiya", "delhi", "mumbai", "bangalore",
    "bengaluru", "chennai", "hyderabad", "kolkata", "pune", "ahmedabad",
    "modi", "bjp", "congress", "rahul", "rahul gandhi", "bse", "nse",
    "sensex", "nifty", "rbi", "sebi", "niti aayog", "pli", "upi",
    "rupee", "inr", "isro", "iit", "iim", "tata", "reliance", "infosys",
    "wipro", "hdfc", "icici", "sbi", "ola", "flipkart", "zomato",
    "swiggy", "byjus", "meesho", "razorpay", "zepto", "zerodha",
]


def apply_india_multipliers(signal: "ScoredSignal") -> "ScoredSignal":
    """
    Apply India-specific multiplier to a scored signal.

    Looks up MULTIPLIERS[steeep_category][temporal_layer] and multiplies
    signal.final_score. Sets signal.india_adjusted = True.

    Args:
        signal: ScoredSignal already base-scored by signal_scorer.py

    Returns:
        ScoredSignal with final_score adjusted and india_adjusted=True
    """
    steeep = signal.steeep_category
    temporal = signal.temporal_layer

    if steeep in MULTIPLIERS and temporal in MULTIPLIERS[steeep]:
        multiplier = MULTIPLIERS[steeep][temporal]
    else:
        multiplier = 1.0  # neutral fallback

    signal.final_score = signal.final_score * multiplier
    signal.india_adjusted = True
    return signal


def get_multiplier(steeep_category: str, temporal_layer: str) -> float:
    """
    Return the India multiplier for a STEEEP×Temporal pair.

    Args:
        steeep_category: Social/Technological/Economic/Environmental/Ethical/Political
        temporal_layer:  Operational/Strategic/Civilizational

    Returns:
        float multiplier (0.85–1.4 range), 1.0 on unknown input
    """
    return MULTIPLIERS.get(steeep_category, {}).get(temporal_layer, 1.0)


def get_top_multipliers(n: int = 2) -> List[Tuple[str, str, float]]:
    """
    Return the top N most impactful India multipliers (by distance from 1.0).

    Used by report_formatter.py for the India Lens section.

    Args:
        n: Number of top multipliers to return (default: 2)

    Returns:
        List of (steeep, temporal, value) tuples sorted by |value - 1.0| desc
    """
    all_mults: List[Tuple[str, str, float]] = []
    for steeep, temporal_dict in MULTIPLIERS.items():
        for temporal, value in temporal_dict.items():
            all_mults.append((steeep, temporal, value))

    all_mults.sort(key=lambda x: abs(x[2] - 1.0), reverse=True)
    return all_mults[:n]


def is_india_relevant(query: str) -> bool:
    """
    Determine whether a query is India-relevant by keyword matching.

    Args:
        query: The foresight query string

    Returns:
        True if India multipliers should be applied
    """
    query_lower = query.lower()
    return any(kw in query_lower for kw in INDIA_KEYWORDS)
