"""
test_probability.py

Unit tests for probability_calc.py and confidence_calc.py.
Tests normalization to 100%, boundary conditions, confidence formula.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from signal_scorer import Signal, score_signal, build_steeep_matrix
from probability_calc import (
    Analogue,
    ProbabilityResult,
    calculate_probabilities,
    calculate_confidence,
    _normalize,
    _probable_raw,
    _plausible_raw,
    _possible_raw,
)
from confidence_calc import calculate_confidence as calc_conf_standalone


def _make_analogue(name="Test", similarity=75.0) -> Analogue:
    return Analogue(
        name=name,
        description="Test analogue",
        conditions_then="Similar conditions",
        tipping_incident="Key event in 2020",
        outcome="Outcome happened",
        similarity_score=similarity,
    )


def _make_signals(n_supporting=5, n_opposing=2, n_wildcard=1, n_neutral=1):
    signals = []
    for _ in range(n_supporting):
        signals.append(score_signal(Signal(
            content="Strong growth investment increase opportunity boost",
            source="Reuters",
            date="2025-06-01",
            signal_type="SUPPORTING",
        )))
    for _ in range(n_opposing):
        signals.append(score_signal(Signal(
            content="Significant decline fall barrier challenge failure",
            source="Bloomberg",
            date="2025-06-01",
            signal_type="OPPOSING",
        )))
    for _ in range(n_wildcard):
        signals.append(score_signal(Signal(
            content="Unexpected collapse disruption black swan crisis",
            source="FT",
            date="2025-06-01",
            signal_type="WILDCARD",
        )))
    for _ in range(n_neutral):
        signals.append(score_signal(Signal(
            content="Mixed results observed across the sector",
            source="Analyst",
            date="2025-06-01",
            signal_type="NEUTRAL",
        )))
    return signals


class TestNormalization(unittest.TestCase):
    """_normalize: three values must sum to exactly 100.0."""

    def test_sums_to_100(self):
        p, pl, po = _normalize(10.0, 5.0, 3.0)
        self.assertAlmostEqual(p + pl + po, 100.0, places=1)

    def test_all_zero_equal_distribution(self):
        p, pl, po = _normalize(0, 0, 0)
        self.assertAlmostEqual(p + pl + po, 100.0, places=1)
        self.assertAlmostEqual(p, 33.3, places=0)

    def test_single_nonzero_gets_100(self):
        p, pl, po = _normalize(5.0, 0, 0)
        self.assertAlmostEqual(p, 100.0, places=1)
        self.assertEqual(pl, 0.0)
        self.assertEqual(po, 0.0)

    def test_sum_always_100(self):
        test_cases = [
            (1, 2, 3), (10, 0, 0), (0, 10, 0), (0, 0, 10),
            (100, 100, 100), (1.5, 2.5, 3.0), (0.1, 0.1, 0.1),
        ]
        for a, b, c in test_cases:
            p, pl, po = _normalize(a, b, c)
            self.assertAlmostEqual(p + pl + po, 100.0, places=1,
                                   msg=f"Failed for {a}, {b}, {c}")

    def test_deterministic(self):
        for _ in range(5):
            r1 = _normalize(7.0, 3.0, 2.0)
            r2 = _normalize(7.0, 3.0, 2.0)
            self.assertEqual(r1, r2)


class TestRawScores(unittest.TestCase):
    """Raw score formulas."""

    def test_probable_raw_increases_with_strong_supporting(self):
        signals_few = _make_signals(n_supporting=1, n_opposing=0, n_wildcard=0, n_neutral=0)
        signals_many = _make_signals(n_supporting=10, n_opposing=0, n_wildcard=0, n_neutral=0)
        # Force scores > 0.7 by using high-quality signals
        matrix_few  = build_steeep_matrix(signals_few)
        matrix_many = build_steeep_matrix(signals_many)
        analogues = [_make_analogue(similarity=80.0)]

        raw_few  = _probable_raw(signals_few,  analogues, matrix_few)
        raw_many = _probable_raw(signals_many, analogues, matrix_many)
        self.assertGreater(raw_many, raw_few)

    def test_possible_raw_increases_with_wildcards(self):
        no_wild   = _make_signals(n_wildcard=0)
        with_wild = _make_signals(n_wildcard=5)
        analogues = []
        matrix_nw = build_steeep_matrix(no_wild)
        matrix_ww = build_steeep_matrix(with_wild)
        raw_nw = _possible_raw(no_wild,   analogues)
        raw_ww = _possible_raw(with_wild, analogues)
        self.assertGreater(raw_ww, raw_nw)

    def test_plausible_raw_with_medium_analogues(self):
        signals = _make_signals(n_supporting=5)
        analogues = [_make_analogue(similarity=55.0), _make_analogue(similarity=60.0)]
        raw = _plausible_raw(signals, analogues)
        self.assertGreater(raw, 0)


class TestCalculateProbabilities(unittest.TestCase):
    """calculate_probabilities: full integration."""

    def _run(self, **kw):
        signals = _make_signals(**kw)
        analogues = [_make_analogue(similarity=75.0), _make_analogue(similarity=50.0)]
        matrix = build_steeep_matrix(signals)
        return calculate_probabilities(matrix, signals, analogues)

    def test_probabilities_sum_to_100(self):
        result = self._run(n_supporting=5, n_opposing=2, n_wildcard=2, n_neutral=1)
        total = result.probable_pct + result.plausible_pct + result.possible_pct
        self.assertAlmostEqual(total, 100.0, places=1)

    def test_returns_probability_result(self):
        result = self._run()
        self.assertIsInstance(result, ProbabilityResult)

    def test_confidence_is_integer_0_to_100(self):
        result = self._run()
        self.assertIsInstance(result.confidence, int)
        self.assertGreaterEqual(result.confidence, 0)
        self.assertLessEqual(result.confidence, 100)

    def test_zero_signals_equal_distribution(self):
        matrix = build_steeep_matrix([])
        result = calculate_probabilities(matrix, [], [])
        total = result.probable_pct + result.plausible_pct + result.possible_pct
        self.assertAlmostEqual(total, 100.0, places=1)

    def test_deterministic(self):
        """Same input → same output every time."""
        signals = _make_signals(n_supporting=8, n_opposing=3, n_wildcard=2, n_neutral=2)
        analogues = [_make_analogue(similarity=70.0)]
        matrix = build_steeep_matrix(signals)
        r1 = calculate_probabilities(matrix, signals, analogues)
        r2 = calculate_probabilities(matrix, signals, analogues)
        self.assertEqual(r1.probable_pct,  r2.probable_pct)
        self.assertEqual(r1.plausible_pct, r2.plausible_pct)
        self.assertEqual(r1.possible_pct,  r2.possible_pct)


class TestCalculateConfidence(unittest.TestCase):
    """calculate_confidence: formula components."""

    def _basic_counts(self, total=15, supporting=10, opposing=3):
        return {"total": total, "SUPPORTING": supporting, "OPPOSING": opposing}

    def test_returns_integer(self):
        matrix = build_steeep_matrix([])
        conf = calculate_confidence(matrix, self._basic_counts(), 75.0)
        self.assertIsInstance(conf, int)

    def test_range_0_to_100(self):
        matrix = build_steeep_matrix([])
        for total, sup, opp, sim in [
            (0, 0, 0, 0),
            (25, 20, 5, 100),
            (100, 50, 50, 50),
        ]:
            conf = calculate_confidence(matrix, {"total": total, "SUPPORTING": sup, "OPPOSING": opp}, sim)
            self.assertGreaterEqual(conf, 0)
            self.assertLessEqual(conf, 100)

    def test_more_signals_higher_density(self):
        matrix = build_steeep_matrix([])
        conf_low  = calculate_confidence(matrix, {"total": 5,  "SUPPORTING": 3, "OPPOSING": 1}, 50.0)
        conf_high = calculate_confidence(matrix, {"total": 25, "SUPPORTING": 20, "OPPOSING": 3}, 50.0)
        self.assertGreater(conf_high, conf_low)

    def test_better_analogue_higher_confidence(self):
        matrix = build_steeep_matrix([])
        counts = self._basic_counts()
        conf_low  = calculate_confidence(matrix, counts, 20.0)
        conf_high = calculate_confidence(matrix, counts, 90.0)
        self.assertGreater(conf_high, conf_low)

    def test_standalone_matches_probability_calc_version(self):
        """confidence_calc.py and probability_calc.py must return same value."""
        matrix = build_steeep_matrix([])
        counts = {"total": 20, "SUPPORTING": 15, "OPPOSING": 5}
        similarity = 70.0
        c1 = calculate_confidence(matrix, counts, similarity)
        c2 = calc_conf_standalone(matrix, counts, similarity)
        self.assertEqual(c1, c2)


class TestIndiaMultiplierEffect(unittest.TestCase):
    """India multipliers should increase scores for relevant cells."""

    def test_technological_operational_gets_higher_score(self):
        """Technological/Operational has 1.4× multiplier — score should be higher with India."""
        s = Signal(
            content="UPI digital payment platform growing",
            source="RBI",
            date="2025-01-01",
            steeep_category="Technological",
            temporal_layer="Operational",
            signal_type="SUPPORTING",
        )
        scored_no_india = score_signal(s, india_relevant=False)
        scored_india    = score_signal(s, india_relevant=True)
        self.assertGreater(scored_india.final_score, scored_no_india.final_score)

    def test_political_operational_gets_lower_score(self):
        """Political/Operational has 0.85× multiplier — score should be lower with India."""
        s = Signal(
            content="Government election political vote parliament",
            source="Economic Times",
            date="2025-01-01",
            steeep_category="Political",
            temporal_layer="Operational",
            signal_type="SUPPORTING",
        )
        scored_no_india = score_signal(s, india_relevant=False)
        scored_india    = score_signal(s, india_relevant=True)
        self.assertLess(scored_india.final_score, scored_no_india.final_score)


if __name__ == "__main__":
    unittest.main(verbosity=2)
