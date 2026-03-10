"""
test_decision_guidance.py

Unit tests for decision_guidance.py
Tests recommended stance logic, risk trigger identification,
low-regret move computation, and confidence tier assignment.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from decision_guidance import (
    compute_recommended_stance,
    compute_low_regret_move,
    compute_risk_trigger,
    compute_confidence_tier,
    compute_guidance,
)


class TestRecommendedStance(unittest.TestCase):
    """Stance logic based on probability percentages."""

    def test_high_probable_gives_directional_stance(self):
        stance = compute_recommended_stance(probable_pct=60, plausible_pct=25)
        self.assertIn("Align", stance)
        self.assertIn("probable", stance.lower())

    def test_high_plausible_gives_hedge_stance(self):
        stance = compute_recommended_stance(probable_pct=40, plausible_pct=40)
        self.assertIn("Hedge", stance)

    def test_mixed_signals_gives_optionality_stance(self):
        stance = compute_recommended_stance(probable_pct=34, plausible_pct=33)
        self.assertIn("optionality", stance.lower())

    def test_exactly_50_probable_is_directional(self):
        # probable_pct > 50 threshold
        stance_51 = compute_recommended_stance(probable_pct=51, plausible_pct=25)
        stance_50 = compute_recommended_stance(probable_pct=50, plausible_pct=25)
        self.assertIn("Align", stance_51)
        self.assertNotIn("Align", stance_50)

    def test_returns_string(self):
        stance = compute_recommended_stance(probable_pct=33, plausible_pct=33)
        self.assertIsInstance(stance, str)
        self.assertGreater(len(stance), 0)


class TestRiskTrigger(unittest.TestCase):
    """Risk trigger identifies highest-scoring OPPOSING signal."""

    def _make_signal(self, signal_type, final_score, content="Default content signal text"):
        return {
            "content": content,
            "signal_type": signal_type,
            "final_score": final_score,
        }

    def test_highest_opposing_signal_selected(self):
        signals = [
            self._make_signal("OPPOSING", 0.5, "Low opposition signal content here"),
            self._make_signal("OPPOSING", 0.9, "High opposition signal content here critical"),
            self._make_signal("SUPPORTING", 0.8, "Supporting signal content not selected"),
        ]
        trigger = compute_risk_trigger(signals)
        self.assertIn("High opposition", trigger)

    def test_no_opposing_falls_back_to_wildcard(self):
        signals = [
            self._make_signal("SUPPORTING", 0.8, "Supporting signal content goes here"),
            self._make_signal("WILDCARD", 0.7, "Wildcard unexpected disruption signal here"),
        ]
        trigger = compute_risk_trigger(signals)
        self.assertIn("Wildcard", trigger)

    def test_no_signals_returns_fallback_string(self):
        trigger = compute_risk_trigger([])
        self.assertIsInstance(trigger, str)
        self.assertGreater(len(trigger), 0)

    def test_long_content_truncated(self):
        long_content = "A" * 200
        signals = [self._make_signal("OPPOSING", 0.8, long_content)]
        trigger = compute_risk_trigger(signals)
        self.assertLessEqual(len(trigger), 130)


class TestLowRegretMove(unittest.TestCase):
    """Low-regret move based on hottest cell and net direction."""

    def test_returns_string(self):
        move = compute_low_regret_move("Technological/Strategic", "SUPPORTING")
        self.assertIsInstance(move, str)
        self.assertGreater(len(move), 0)

    def test_supporting_direction_mentioned(self):
        move = compute_low_regret_move("Technological/Strategic", "SUPPORTING")
        self.assertIn("accelerated", move.lower())

    def test_opposing_direction_mentioned(self):
        move = compute_low_regret_move("Economic/Operational", "OPPOSING")
        self.assertIn("optionality", move.lower())

    def test_all_steeep_categories_handled(self):
        from signal_scorer import STEEEP_CATEGORIES, TEMPORAL_LAYERS
        for steeep in STEEEP_CATEGORIES:
            for temporal in TEMPORAL_LAYERS:
                move = compute_low_regret_move(f"{steeep}/{temporal}", "NEUTRAL")
                self.assertIsInstance(move, str)
                self.assertGreater(len(move), 0)


class TestConfidenceTier(unittest.TestCase):
    """Confidence tier classification."""

    def test_high_confidence_high_probable_gives_HIGH(self):
        tier = compute_confidence_tier(confidence_score=75, signals_count=20, probable_pct=55)
        self.assertEqual(tier, "HIGH")

    def test_low_score_gives_LOW(self):
        tier = compute_confidence_tier(confidence_score=30, signals_count=15, probable_pct=45)
        self.assertEqual(tier, "LOW")

    def test_few_signals_gives_LOW(self):
        tier = compute_confidence_tier(confidence_score=80, signals_count=5, probable_pct=60)
        self.assertEqual(tier, "LOW")

    def test_medium_confidence_gives_MEDIUM(self):
        tier = compute_confidence_tier(confidence_score=55, signals_count=15, probable_pct=45)
        self.assertEqual(tier, "MEDIUM")

    def test_tier_values_are_valid(self):
        valid_tiers = {"HIGH", "MEDIUM", "LOW"}
        for score in [0, 35, 50, 71, 100]:
            for signals in [5, 15, 30]:
                for prob in [20, 40, 55]:
                    tier = compute_confidence_tier(score, signals, prob)
                    self.assertIn(tier, valid_tiers)


class TestComputeGuidanceIntegration(unittest.TestCase):
    """Integration test for full guidance computation."""

    def _make_inputs(self):
        probabilities = {
            "probable_pct": 55,
            "plausible_pct": 30,
            "possible_pct": 15,
            "confidence": 72,
        }
        matrix = {
            "hottest_cell": "Technological/Strategic",
            "net_direction": "SUPPORTING",
        }
        signals = [
            {"content": "EV adoption accelerating in 2025 globally",
             "signal_type": "SUPPORTING", "final_score": 0.85},
            {"content": "Supply chain constraints remain a significant barrier",
             "signal_type": "OPPOSING", "final_score": 0.72},
            {"content": "Battery costs fell 40% since 2020 per BloombergNEF",
             "signal_type": "SUPPORTING", "final_score": 0.90},
        ]
        return probabilities, matrix, signals

    def test_guidance_has_required_keys(self):
        probs, matrix, signals = self._make_inputs()
        guidance = compute_guidance(probs, matrix, signals, confidence_score=72)
        required_keys = [
            "recommended_stance", "low_regret_move", "risk_trigger",
            "dominant_matrix_zone", "confidence_in_guidance"
        ]
        for key in required_keys:
            self.assertIn(key, guidance)

    def test_guidance_values_are_strings(self):
        probs, matrix, signals = self._make_inputs()
        guidance = compute_guidance(probs, matrix, signals, confidence_score=72)
        for key in ["recommended_stance", "low_regret_move", "risk_trigger"]:
            self.assertIsInstance(guidance[key], str)
            self.assertGreater(len(guidance[key]), 0)

    def test_high_probable_gives_directional_guidance(self):
        probs, matrix, signals = self._make_inputs()
        guidance = compute_guidance(probs, matrix, signals, confidence_score=72)
        self.assertIn("Align", guidance["recommended_stance"])

    def test_risk_trigger_identifies_opposing_signal(self):
        probs, matrix, signals = self._make_inputs()
        guidance = compute_guidance(probs, matrix, signals, confidence_score=72)
        # The opposing signal content should appear in risk_trigger
        self.assertIn("Supply chain", guidance["risk_trigger"])

    def test_dominant_zone_set_correctly(self):
        probs, matrix, signals = self._make_inputs()
        guidance = compute_guidance(probs, matrix, signals, confidence_score=72)
        self.assertEqual(guidance["dominant_matrix_zone"], "Technological/Strategic")


if __name__ == "__main__":
    unittest.main(verbosity=2)
