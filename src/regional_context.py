#!/usr/bin/env python3
"""
regional_context.py - Route to correct regional context file.
Pure arithmetic routing. No AI. No web calls.
Author: Santhosh Gandhi

Usage: python src/regional_context.py [region_string]
Output: multiplier dict to stdout
"""

import sys
import json
from typing import Dict

# Region detection keywords
_REGION_KEYWORDS = {
    "india": ["india", "indian", "bharat", "mumbai", "delhi", "bangalore",
              "bengaluru", "chennai", "rupee", "inr", "isro", "nasscom",
              "tata", "reliance", "infosys", "flipkart", "upi"],
    "usa": ["usa", "us ", "america", "american", "dollar", "washington",
            "silicon valley", "nasdaq", "s&p", "federal reserve", "u.s.",
            "new york", "california", "congress", "white house"],
    "europe": ["europe", "european", "eu ", "euro", "germany", "france",
               "uk ", "britain", "london", "paris", "berlin", "brussels",
               "ecb", "eurozone", "brexit", "gdpr"],
    "china": ["china", "chinese", "beijing", "shanghai", "yuan", "renminbi",
              "ccp", "alibaba", "tencent", "huawei", "byd", "baidu"],
}


def detect_region(text: str) -> str:
    """
    Detect region from query or signal text.

    Args:
        text: Query string or combined signal content

    Returns:
        Region string: 'india', 'usa', 'europe', 'china', or 'global'
    """
    text_lower = text.lower()
    for region, keywords in _REGION_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return region
    return "global"


def get_multipliers(region: str) -> Dict[str, Dict[str, float]]:
    """
    Import and return multipliers from the matching context file.

    Args:
        region: Region string ('india', 'usa', 'europe', 'china', or 'global')

    Returns:
        Dict of STEEEP -> temporal -> multiplier
    """
    region_lower = region.lower() if region else "global"

    try:
        import os
        import importlib.util

        # Build path to contexts directory
        src_dir = os.path.dirname(os.path.abspath(__file__))
        contexts_dir = os.path.join(os.path.dirname(src_dir), "contexts")

        context_map = {
            "india": "india",
            "usa": "usa",
            "europe": "europe",
            "china": "china",
            "global": "global_default",
        }

        module_name = context_map.get(region_lower, "global_default")
        module_path = os.path.join(contexts_dir, f"{module_name}.py")

        if os.path.exists(module_path):
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod.MULTIPLIERS
        else:
            return _global_default_multipliers()

    except Exception:
        return _global_default_multipliers()


def _global_default_multipliers() -> Dict[str, Dict[str, float]]:
    """Fallback: all multipliers = 1.0"""
    dims = ["Social", "Technological", "Economic", "Environmental", "Ethical", "Political"]
    layers = ["Operational", "Strategic", "Civilizational"]
    return {d: {l: 1.0 for l in layers} for d in dims}


def get_top_multipliers(region: str, n: int = 2):
    """
    Return the top N most impactful multipliers (by distance from 1.0).

    Args:
        region: Region string
        n: Number of top multipliers to return

    Returns:
        List of (steeep, temporal, value) tuples sorted by |value - 1.0| desc
    """
    multipliers = get_multipliers(region)
    all_mults = []
    for steeep, temporal_dict in multipliers.items():
        for temporal, value in temporal_dict.items():
            all_mults.append((steeep, temporal, value))
    all_mults.sort(key=lambda x: abs(x[2] - 1.0), reverse=True)
    return all_mults[:n]


def main():
    if len(sys.argv) < 2:
        region = "global"
    else:
        region = detect_region(" ".join(sys.argv[1:]))

    multipliers = get_multipliers(region)
    result = {
        "region": region,
        "multipliers": multipliers,
        "top_movers": [
            {"steeep": s, "temporal": t, "value": v}
            for s, t, v in get_top_multipliers(region, 3)
        ],
    }
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
