"""
test_confidence.py

Unit tests for confidence_calc.py
Tests score range, zero-signal edge case, max-signal near-100,
and three sub-score contributions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from signal_scorer import STEEEP_CATEGORIES, TEMPORAL_LAYERS, MatrixCell, Matrix
from confidence_calc import calculate_confidence


def _make_matrix(signal_counts=None, cells_override=None):
    """Build a minimal Matrix for testing."""
    sc = signal_counts or {"total": 0, "SUPPORTING": 0, "OPPOSING": 0,
                           "NEUTRAL": 0, "WILDCARD": 0}
    cells = {
        f"{s}/{t}": MatrixCell(steeep=s, temporal=t, score=0.0, signal_count=0)
        for s in STEEEP_CATEGORIES for t in TEMPORAL_LAYERS
    }
    if cells_override:
        cells.update(cells_override)
    return Matrix(
        cells=cells,
        hottest_cell="Technological/Strategic",
        net_direction="NEUTRAL",
        blind_zones=[],
        signal_counts=sc,
    )


class TestConfidenceRange(unittest.TestCase):
    """Score must always be in [0, 100]."""

    def test_zero_signals_returns_zero(self):
        matrix = _make_matrix({"total": 0, "SUPPORTING": 0, "OPPOSING": 0,
                                "NEUTRAL": 0, "WILDCARD": 0})
        score = calculate_confidence(matrix, matrix.signal_counts, 0.0)
        self.assertEqual(score, 0)

    def test_never_exceeds_100(self):
        sc = {"total": 1000, "SUPPORTING": 999, "OPPOSING": 1,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        score = calculate_confidence(matrix, sc, 100.0)
        self.assertLessEqual(score, 100)

    def test_always_non_negative(self):
        sc = {"total": 5, "SUPPORTING": 2, "OPPOSING": 3, "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        score = calculate_confidence(matrix, sc, 0.0)
        self.assertGreaterEqual(score, 0)

    def test_returns_integer(self):
        sc = {"total": 10, "SUPPORTING": 8, "OPPOSING": 2, "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        score = calculate_confidence(matrix, sc, 75.0)
        self.assertIsInstance(score, int)


class TestSignalDensityComponent(unittest.TestCase):
    """Signal density sub-score: 0-40."""

    def test_25_signals_maxes_density(self):
        sc = {"total": 25, "SUPPORTING": 12, "OPPOSING": 8,
              "NEUTRAL": 5, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        # density = min(40, 25/25*40) = 40
        # With 0 analogue similarity: confidence >= 40
        score = calculate_confidence(matrix, sc, 0.0)
        self.assertGreaterEqual(score, 40)

    def test_50_signals_still_caps_at_40(self):
        sc = {"total": 50, "SUPPORTING": 25, "OPPOSING": 25,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        score_50 = calculate_confidence(matrix, sc, 0.0)

        sc2 = {"total": 25, "SUPPORTING": 12, "OPPOSING": 12,
               "NEUTRAL": 1, "WILDCARD": 0}
        matrix2 = _make_matrix(sc2)
        score_25 = calculate_confidence(matrix2, sc2, 0.0)

        # Density component is same (both hit cap at 40)
        # Balance component is also same (equal distribution)
        self.assertEqual(score_50, score_25)


class TestEvidenceBalanceComponent(unittest.TestCase):
    """Evidence balance sub-score: 0-30."""

    def test_perfectly_balanced_gives_zero_balance(self):
        sc = {"total": 20, "SUPPORTING": 10, "OPPOSING": 10,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        # balance = |10-10|/20 * 30 = 0
        # density = 20/25*40 = 32
        # With 0 analogue: score = 32
        score = calculate_confidence(matrix, sc, 0.0)
        self.assertAlmostEqual(score, 32, delta=2)

    def test_all_supporting_gives_max_balance(self):
        sc = {"total": 25, "SUPPORTING": 25, "OPPOSING": 0,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        # density = 40, balance = 25/25*30 = 30 -> total 70 (no historical)
        score = calculate_confidence(matrix, sc, 0.0)
        self.assertAlmostEqual(score, 70, delta=2)


class TestHistoricalGroundingComponent(unittest.TestCase):
    """Historical grounding sub-score: 0-30."""

    def test_100_similarity_gives_30_grounding(self):
        sc = {"total": 0, "SUPPORTING": 0, "OPPOSING": 0,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        # density = 0, balance = 0, grounding = 30
        score = calculate_confidence(matrix, sc, 100.0)
        self.assertEqual(score, 30)

    def test_50_similarity_gives_15_grounding(self):
        sc = {"total": 0, "SUPPORTING": 0, "OPPOSING": 0,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        # density=0, balance=0, grounding=15
        score = calculate_confidence(matrix, sc, 50.0)
        self.assertAlmostEqual(score, 15, delta=1)

    def test_zero_similarity_gives_zero_grounding(self):
        sc = {"total": 0, "SUPPORTING": 0, "OPPOSING": 0,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        score = calculate_confidence(matrix, sc, 0.0)
        self.assertEqual(score, 0)


class TestThreeSubScoresSumCorrectly(unittest.TestCase):
    """Verify all three components add up as expected."""

    def test_components_sum_to_total(self):
        sc = {"total": 20, "SUPPORTING": 15, "OPPOSING": 5,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)

        density = min(40.0, (20 / 25.0) * 40.0)       # 32.0
        balance = (abs(15 - 5) / 20) * 30.0            # 15.0
        grounding = (80.0 / 100.0) * 30.0              # 24.0
        expected = min(100, int(round(density + balance + grounding)))  # 71

        score = calculate_confidence(matrix, sc, 80.0)
        self.assertEqual(score, expected)

    def test_max_all_three_components(self):
        sc = {"total": 25, "SUPPORTING": 25, "OPPOSING": 0,
              "NEUTRAL": 0, "WILDCARD": 0}
        matrix = _make_matrix(sc)
        # density=40, balance=30, grounding=30 -> 100
        score = calculate_confidence(matrix, sc, 100.0)
        self.assertEqual(score, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
