"""
contexts/china.py - China regional context multipliers.
Author: Santhosh Gandhi
"""

MULTIPLIERS = {
    "Social": {
        "Operational":    0.9,   # aging population, youth unemployment pressure
        "Strategic":      1.0,
        "Civilizational": 1.1,   # civilizational identity, cultural continuity
    },
    "Technological": {
        "Operational":    1.3,   # manufacturing scale, EV/solar dominance
        "Strategic":      1.5,   # state-directed innovation, AI investment scale
        "Civilizational": 1.3,   # semiconductor catch-up, space program
    },
    "Economic": {
        "Operational":    1.2,   # manufacturing scale, export dominance
        "Strategic":      1.3,   # domestic market depth, Belt and Road reach
        "Civilizational": 1.1,   # yuan internationalization push
    },
    "Environmental": {
        "Operational":    0.8,   # enforcement gaps, coal dependency
        "Strategic":      1.1,   # renewable energy investment scale
        "Civilizational": 1.2,   # solar/wind manufacturing leadership
    },
    "Ethical": {
        "Operational":    0.7,   # regulatory opacity, data control
        "Strategic":      0.8,
        "Civilizational": 0.9,
    },
    "Political": {
        "Operational":    1.3,   # state capacity, policy execution speed
        "Strategic":      1.3,   # long-term planning advantage, 5-year plans
        "Civilizational": 1.2,   # civilizational state model
    },
}

CONTEXT_NOTES = {
    "Technological_Strategic":  "State-directed AI and semiconductor investment scale",
    "Political_Operational":    "State capacity enables rapid policy execution",
    "Ethical_Operational":      "Regulatory opacity and data control discount",
    "Environmental_Operational": "Enforcement gaps on coal phase-out",
}
