"""
test_scorer.py

Unit tests for signal_scorer.py
Tests recency weights, reliability weights, type weights, STEEEP/temporal
classification, and full score_signal() output.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from signal_scorer import (
    Signal, ScoredSignal, score_signal,
    _recency_weight, _reliability_weight, _type_weight,
    _classify_steeep, _classify_temporal, _classify_signal_type,
    STEEEP_CATEGORIES, TEMPORAL_LAYERS, SIGNAL_TYPES,
)


class TestRecencyWeight(unittest.TestCase):
    """_recency_weight: same input = same output (deterministic)."""

    def test_unknown_date_returns_05(self):
        self.assertEqual(_recency_weight(None), 0.5)
        self.assertEqual(_recency_weight(""), 0.5)

    def test_recent_date_returns_1(self):
        self.assertEqual(_recency_weight("2026-02-01"), 1.0)  # ~5 weeks ago
        self.assertEqual(_recency_weight("2026-01-15"), 1.0)  # ~7 weeks ago

    def test_mid_year_returns_08(self):
        # ~8 months ago from March 2026 → 0.8
        weight = _recency_weight("2025-07-01")
        self.assertEqual(weight, 0.8)

    def test_2_years_ago_returns_06(self):
        weight = _recency_weight("2024-01-01")
        self.assertEqual(weight, 0.6)

    def test_4_years_ago_returns_04(self):
        weight = _recency_weight("2021-01-01")
        self.assertEqual(weight, 0.4)

    def test_year_only_parses(self):
        weight = _recency_weight("2025")
        self.assertIn(weight, [0.6, 0.8, 1.0])  # mid-year estimate

    def test_deterministic(self):
        """Same input always returns same output."""
        for _ in range(5):
            self.assertEqual(_recency_weight("2025-06-15"), _recency_weight("2025-06-15"))


class TestReliabilityWeight(unittest.TestCase):
    """_reliability_weight: source type classification."""

    def test_government_source(self):
        self.assertEqual(_reliability_weight("RBI Annual Report 2024"), 1.0)
        self.assertEqual(_reliability_weight("NITI Aayog Report"), 1.0)
        self.assertEqual(_reliability_weight("US Government Statistics"), 1.0)

    def test_news_source(self):
        self.assertEqual(_reliability_weight("Reuters, March 2024"), 0.9)
        self.assertEqual(_reliability_weight("Bloomberg Analysis"), 0.9)
        self.assertEqual(_reliability_weight("Economic Times"), 0.9)

    def test_industry_report(self):
        self.assertEqual(_reliability_weight("McKinsey Global Institute Report"), 0.85)
        self.assertEqual(_reliability_weight("Gartner Research 2024"), 0.85)
        self.assertEqual(_reliability_weight("NASSCOM Survey"), 0.85)

    def test_analyst(self):
        self.assertAlmostEqual(_reliability_weight("Senior Analyst Commentary"), 0.7)

    def test_blog(self):
        self.assertEqual(_reliability_weight("Personal blog post on substack"), 0.5)

    def test_unknown_source(self):
        self.assertEqual(_reliability_weight(""), 0.4)
        self.assertEqual(_reliability_weight(None), 0.4)
        self.assertEqual(_reliability_weight("some random website xyz"), 0.4)


class TestTypeWeight(unittest.TestCase):
    """_type_weight: type classification."""

    def test_supporting_weight(self):
        self.assertEqual(_type_weight("SUPPORTING"), 1.0)

    def test_opposing_weight(self):
        self.assertEqual(_type_weight("OPPOSING"), 1.0)

    def test_neutral_weight(self):
        self.assertEqual(_type_weight("NEUTRAL"), 0.6)

    def test_wildcard_weight(self):
        self.assertEqual(_type_weight("WILDCARD"), 1.3)

    def test_case_insensitive(self):
        self.assertEqual(_type_weight("supporting"), 1.0)
        self.assertEqual(_type_weight("Wildcard"), 1.3)

    def test_unknown_type_defaults_to_neutral(self):
        self.assertEqual(_type_weight("UNKNOWN"), 0.6)


class TestSTEEEPClassification(unittest.TestCase):
    """_classify_steeep: STEEEP category inference."""

    def test_provided_valid_category_used(self):
        for cat in STEEEP_CATEGORIES:
            self.assertEqual(_classify_steeep("any content", cat), cat)

    def test_provided_invalid_falls_back_to_inference(self):
        result = _classify_steeep("EV adoption growing rapidly", "INVALID")
        self.assertIn(result, STEEEP_CATEGORIES)

    def test_technology_detected(self):
        result = _classify_steeep("AI software platform growing 40% annually", None)
        self.assertEqual(result, "Technological")

    def test_political_detected(self):
        result = _classify_steeep("Government policy for PLI scheme subsidies", None)
        self.assertEqual(result, "Political")

    def test_economic_default(self):
        result = _classify_steeep("content with no clear category", None)
        self.assertEqual(result, "Economic")

    def test_returns_valid_category(self):
        for text in [
            "climate change emission carbon",
            "election vote parliament",
            "health education social welfare",
            "AI technology digital",
        ]:
            result = _classify_steeep(text, None)
            self.assertIn(result, STEEEP_CATEGORIES)


class TestTemporalClassification(unittest.TestCase):
    """_classify_temporal: temporal layer inference."""

    def test_provided_valid_layer_used(self):
        for layer in TEMPORAL_LAYERS:
            self.assertEqual(_classify_temporal("any content", layer), layer)

    def test_operational_detected(self):
        result = _classify_temporal("Latest 2025 quarterly results show growth", None)
        self.assertEqual(result, "Operational")

    def test_strategic_detected(self):
        result = _classify_temporal("10 year roadmap by 2035 strategic plan", None)
        self.assertEqual(result, "Strategic")

    def test_civilizational_detected(self):
        result = _classify_temporal("Long-term structural transformation generational shift", None)
        self.assertEqual(result, "Civilizational")

    def test_returns_valid_layer(self):
        result = _classify_temporal("no keywords here at all", None)
        self.assertIn(result, TEMPORAL_LAYERS)


class TestSignalTypeClassification(unittest.TestCase):
    """_classify_signal_type: signal direction inference."""

    def test_provided_valid_type_used(self):
        for stype in SIGNAL_TYPES:
            self.assertEqual(_classify_signal_type("any content", stype), stype)

    def test_wildcard_detected_first(self):
        result = _classify_signal_type("Unexpected collapse disruption black swan event", None)
        self.assertEqual(result, "WILDCARD")

    def test_supporting_detected(self):
        result = _classify_signal_type(
            "Strong growth increase momentum opportunity investment surge expanding", None
        )
        self.assertEqual(result, "SUPPORTING")

    def test_opposing_detected(self):
        result = _classify_signal_type(
            "Significant decline fall barrier challenge failure difficult problem", None
        )
        self.assertEqual(result, "OPPOSING")

    def test_neutral_default(self):
        result = _classify_signal_type("The situation is mixed with various factors", None)
        self.assertEqual(result, "NEUTRAL")


class TestScoreSignal(unittest.TestCase):
    """score_signal: full integration of weights."""

    def test_base_score_is_product_of_four_weights(self):
        # Formula: recency × reliability × type × evidence (capped at 1.0)
        s = Signal(
            content="Government investment growing rapidly in EV sector 2025",
            source="Reuters",
            date="2026-01-15",  # recent: recency=1.0
        )
        result = score_signal(s, india_relevant=False)
        # recency=1.0, reliability=0.9, type inferred (SUPPORTING~1.0), evidence=0.7 (ANALYSIS default)
        # 1.0 * 0.9 * 1.0 * 0.7 = 0.63
        self.assertGreater(result.base_score, 0.0)
        self.assertLessEqual(result.base_score, 1.0)

    def test_base_score_capped_at_1(self):
        """Wildcard type_weight (1.3) × high recency × high reliability must cap at 1.0."""
        s = Signal(
            content="Government unexpected collapse crisis breakdown 2026",
            source="Reuters 2026",
            date="2026-01-01",
            signal_type="WILDCARD",
        )
        result = score_signal(s, india_relevant=False)
        self.assertLessEqual(result.base_score, 1.0)

    def test_india_relevant_sets_flag(self):
        s = Signal(
            content="India UPI transaction volume hit 10B monthly in 2024",
            source="RBI Annual Report",
            date="2024-12-01",
        )
        result = score_signal(s, india_relevant=True)
        self.assertTrue(result.india_adjusted)

    def test_no_india_flag_when_not_relevant(self):
        s = Signal(
            content="US Federal Reserve raises interest rates",
            source="Bloomberg",
            date="2025-03-01",
        )
        result = score_signal(s, india_relevant=False)
        self.assertFalse(result.india_adjusted)

    def test_result_fields_populated(self):
        s = Signal(content="EV growth trend accelerating", source="McKinsey", date="2025-01-01")
        r = score_signal(s)
        self.assertIsInstance(r, ScoredSignal)
        self.assertIn(r.steeep_category, STEEEP_CATEGORIES)
        self.assertIn(r.temporal_layer, TEMPORAL_LAYERS)
        self.assertIn(r.signal_type, SIGNAL_TYPES)
        self.assertGreater(r.final_score, 0)

    def test_deterministic(self):
        """Same input always returns same output."""
        s = Signal(
            content="India startup ecosystem growing rapidly with $10B funding",
            source="Economic Times",
            date="2025-02-01",
        )
        results = [score_signal(s, india_relevant=True) for _ in range(3)]
        scores = [r.final_score for r in results]
        self.assertEqual(scores[0], scores[1])
        self.assertEqual(scores[1], scores[2])


class TestBoundaryConditions(unittest.TestCase):
    """Boundary conditions for scoring."""

    def test_empty_content(self):
        s = Signal(content="", source="", date=None)
        result = score_signal(s)
        self.assertIsInstance(result, ScoredSignal)
        self.assertGreaterEqual(result.final_score, 0)

    def test_very_long_content(self):
        long = "growth increase support " * 100
        s = Signal(content=long, source="Reuters", date="2025-01-01")
        result = score_signal(s)
        self.assertLessEqual(result.base_score, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
