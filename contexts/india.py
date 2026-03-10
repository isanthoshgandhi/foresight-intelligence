"""
contexts/india.py - India regional context multipliers.
Author: Santhosh Gandhi

Multiplier guide:
  > 1.0  India has asymmetric advantage or elevated exposure in this cell
  < 1.0  India has structural disadvantage or dampening factor
  = 1.0  Neutral — India tracks global baseline
"""

MULTIPLIERS = {
    "Social": {
        "Operational":    1.1,   # rising aspiration, urban-rural gap
        "Strategic":      1.3,   # demographic dividend, rising middle class
        "Civilizational": 1.2,   # language/identity diversity, cultural depth
    },
    "Technological": {
        "Operational":    1.4,   # UPI/DPI advantage, mobile-first adoption
        "Strategic":      1.3,   # deep software talent pool, IT services scale
        "Civilizational": 0.9,   # hardware manufacturing gap, semiconductor dependency
    },
    "Economic": {
        "Operational":    1.0,   # neutral — tracks global cycles
        "Strategic":      1.3,   # large domestic market (1.4B consumers), PLI push
        "Civilizational": 0.9,   # cost arbitrage compressing, commodity import dependency
    },
    "Environmental": {
        "Operational":    0.9,   # policy lag, enforcement gaps
        "Strategic":      1.0,   # neutral — renewable push vs coal dependency
        "Civilizational": 1.1,   # climate vulnerability high (monsoon, coastal, heat stress)
    },
    "Ethical": {
        "Operational":    0.9,   # regulatory unpredictability, enforcement gaps
        "Strategic":      1.0,   # neutral — digital rights framework emerging
        "Civilizational": 1.0,   # neutral — complex multi-stakeholder landscape
    },
    "Political": {
        "Operational":    0.85,  # regulatory unpredictability, state-federal friction
        "Strategic":      1.2,   # PLI scheme industrial policy tailwind, reform momentum
        "Civilizational": 1.15,  # US-China positioning advantage for India
    },
}

CONTEXT_NOTES = {
    "Technological_Operational":    "UPI/DPI infrastructure advantage",
    "Technological_Strategic":      "Deep software talent pool",
    "Technological_Civilizational": "Hardware manufacturing gap",
    "Economic_Strategic":           "Large domestic market — 1.4B consumers",
    "Political_Operational":        "Regulatory unpredictability discount",
    "Political_Strategic":          "PLI scheme industrial policy tailwind",
    "Political_Civilizational":     "US-China positioning advantage for India",
}
