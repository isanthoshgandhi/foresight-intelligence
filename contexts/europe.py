"""
contexts/europe.py - Europe regional context multipliers.
Author: Santhosh Gandhi
"""

MULTIPLIERS = {
    "Social": {
        "Operational":    1.0,
        "Strategic":      1.0,
        "Civilizational": 1.1,   # aging population, migration reshaping
    },
    "Technological": {
        "Operational":    1.1,
        "Strategic":      1.2,   # industrial tech, precision engineering
        "Civilizational": 1.0,
    },
    "Economic": {
        "Operational":    1.0,
        "Strategic":      1.0,
        "Civilizational": 0.9,   # competitiveness concerns vs US/China
    },
    "Environmental": {
        "Operational":    1.3,   # Green Deal, carbon border adjustments active
        "Strategic":      1.4,   # EU regulatory leadership in climate policy
        "Civilizational": 1.3,   # structural green transition commitment
    },
    "Ethical": {
        "Operational":    1.2,   # GDPR, AI Act, regulatory leadership
        "Strategic":      1.3,   # EU as global regulatory standard-setter
        "Civilizational": 1.2,   # rights-based framework strength
    },
    "Political": {
        "Operational":    1.0,
        "Strategic":      1.1,   # European sovereignty push, defense spending
        "Civilizational": 1.1,   # EU integration depth, shared institutions
    },
}

CONTEXT_NOTES = {
    "Environmental_Strategic":  "EU Green Deal and carbon border adjustment leadership",
    "Ethical_Strategic":        "EU as global regulatory standard-setter (GDPR, AI Act)",
    "Economic_Civilizational":  "Competitiveness gap vs US/China on frontier tech",
}
