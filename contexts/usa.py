"""
contexts/usa.py - USA regional context multipliers.
Author: Santhosh Gandhi
"""

MULTIPLIERS = {
    "Social": {
        "Operational":    1.0,
        "Strategic":      1.1,
        "Civilizational": 1.0,
    },
    "Technological": {
        "Operational":    1.3,   # frontier AI, semiconductor leadership
        "Strategic":      1.4,   # innovation ecosystem, VC capital depth
        "Civilizational": 1.2,   # platform entrenchment, IP dominance
    },
    "Economic": {
        "Operational":    1.2,   # reserve currency, consumer market depth
        "Strategic":      1.2,   # domestic demand scale, capital markets
        "Civilizational": 1.0,   # debt concerns, de-dollarization headwind
    },
    "Environmental": {
        "Operational":    0.9,   # policy inconsistency (federal vs state)
        "Strategic":      1.0,
        "Civilizational": 1.1,   # climate transition investment scale
    },
    "Ethical": {
        "Operational":    1.0,
        "Strategic":      1.0,
        "Civilizational": 1.0,
    },
    "Political": {
        "Operational":    0.9,   # political polarization discount
        "Strategic":      1.0,
        "Civilizational": 1.0,
    },
}

CONTEXT_NOTES = {
    "Technological_Strategic":  "VC ecosystem and frontier AI leadership",
    "Economic_Operational":     "Reserve currency and deep capital markets advantage",
    "Political_Operational":    "Political polarization creates policy uncertainty",
}
