"""
test_matrix.py

Unit tests for matrix_builder.py and signal_scorer.build_steeep_matrix().
Tests 18-cell structure, hottest cell, net direction, blind zones,
and boundary conditions (0 signals, all same category).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from signal_scorer import (
    Signal, ScoredSignal, score_signal, build_steeep_matrix,
    Matrix, STEEEP_CATEGORIES, TEMPORAL_LAYERS,
)
from matrix_builder import build_matrix, get_matrix_summary, get_dominant_zone


def _make_scored(
    content="Growth increasing investment",
    source="Reuters",
    date="2025-01-01",
    steeep=None,
    temporal=None,
    sig_type=None,
) -> ScoredSignal:
    s = Signal(
        content=content,
        source=source,
        date=date,
        steeep_category=steeep,
        temporal_layer=temporal,
        signal_type=sig_type,
    )
    return score_signal(s)


class TestMatrixStructure(unittest.TestCase):
    """Matrix must always have exactly 18 cells."""

    def test_18_cells_always_present(self):
        signals = [_make_scored() for _ in range(5)]
        matrix = build_steeep_matrix(signals)
        self.assertEqual(len(matrix.cells), 18)

    def test_all_18_keys_present(self):
        matrix = build_steeep_matrix([])
        expected_keys = {
            f"{s}/{t}" for s in STEEEP_CATEGORIES for t in TEMPORAL_LAYERS
        }
        self.assertEqual(set(matrix.cells.keys()), expected_keys)

    def test_zero_signals_all_blind(self):
        matrix = build_steeep_matrix([])
        self.assertEqual(len(matrix.blind_zones), 18)
        self.assertEqual(matrix.signal_counts["total"], 0)

    def test_zero_signals_net_direction_neutral(self):
        matrix = build_steeep_matrix([])
        self.assertEqual(matrix.net_direction, "NEUTRAL")


class TestCellScores(unittest.TestCase):
    """Cell scores = sum of final_scores of signals in that cell."""

    def test_cell_score_equals_sum_of_signal_scores(self):
        # Force two signals into same cell
        s1 = Signal(
            content="AI software platform growing", source="Reuters",
            date="2025-01-01", steeep_category="Technological", temporal_layer="Strategic",
            signal_type="SUPPORTING",
        )
        s2 = Signal(
            content="Tech investment surge", source="Bloomberg",
            date="2025-02-01", steeep_category="Technological", temporal_layer="Strategic",
            signal_type="SUPPORTING",
        )
        scored = [score_signal(s) for s in [s1, s2]]
        matrix = build_steeep_matrix(scored)

        key = "Technological/Strategic"
        expected = sum(s.final_score for s in scored)
        self.assertAlmostEqual(matrix.cells[key].score, expected, places=6)
        self.assertEqual(matrix.cells[key].signal_count, 2)

    def test_signal_count_totals_correctly(self):
        signals = [_make_scored() for _ in range(10)]
        matrix = build_steeep_matrix(signals)
        self.assertEqual(matrix.signal_counts["total"], 10)


class TestHottestCell(unittest.TestCase):
    """Hottest cell has the highest aggregate score."""

    def test_hottest_cell_has_max_score(self):
        signals = [_make_scored() for _ in range(20)]
        matrix = build_steeep_matrix(signals)
        hot_score = matrix.cells[matrix.hottest_cell].score
        for key, cell in matrix.cells.items():
            self.assertLessEqual(cell.score, hot_score + 1e-9)

    def test_hottest_cell_is_valid_key(self):
        signals = [_make_scored() for _ in range(5)]
        matrix = build_steeep_matrix(signals)
        self.assertIn(matrix.hottest_cell, matrix.cells)


class TestNetDirection(unittest.TestCase):
    """Net direction reflects overall signal balance."""

    def test_all_supporting_gives_supporting_net(self):
        signals = [
            score_signal(Signal(
                content="Strong growth investment increase",
                source="Reuters", date="2025-01-01",
                signal_type="SUPPORTING",
            ))
            for _ in range(10)
        ]
        matrix = build_steeep_matrix(signals)
        self.assertEqual(matrix.net_direction, "SUPPORTING")

    def test_all_opposing_gives_opposing_net(self):
        signals = [
            score_signal(Signal(
                content="Significant decline fall barrier challenge failure",
                source="Bloomberg", date="2025-01-01",
                signal_type="OPPOSING",
            ))
            for _ in range(10)
        ]
        matrix = build_steeep_matrix(signals)
        self.assertEqual(matrix.net_direction, "OPPOSING")

    def test_equal_supporting_opposing_gives_neutral(self):
        sup = score_signal(Signal(
            content="Growth increase opportunity expanding",
            source="Reuters", date="2025-01-01", signal_type="SUPPORTING",
        ))
        opp = score_signal(Signal(
            content="Decline fall barrier obstacle challenge",
            source="Reuters", date="2025-01-01", signal_type="OPPOSING",
        ))
        # Equal counts → neutral
        matrix = build_steeep_matrix([sup, opp])
        self.assertEqual(matrix.net_direction, "NEUTRAL")


class TestBlindZones(unittest.TestCase):
    """Blind zones are cells with zero signals."""

    def test_full_coverage_no_blind_zones(self):
        # Provide signals for every STEEEP×Temporal combination
        signals = []
        for steeep in STEEEP_CATEGORIES:
            for temporal in TEMPORAL_LAYERS:
                signals.append(
                    score_signal(Signal(
                        content="growth increase",
                        source="Reuters",
                        date="2025-01-01",
                        steeep_category=steeep,
                        temporal_layer=temporal,
                    ))
                )
        matrix = build_steeep_matrix(signals)
        self.assertEqual(len(matrix.blind_zones), 0)

    def test_partial_coverage_has_blind_zones(self):
        # Only one cell covered
        s = Signal(
            content="AI growth", source="Reuters", date="2025-01-01",
            steeep_category="Technological", temporal_layer="Strategic",
        )
        matrix = build_steeep_matrix([score_signal(s)])
        self.assertGreater(len(matrix.blind_zones), 0)
        self.assertLessEqual(len(matrix.blind_zones), 17)


class TestSignalCounts(unittest.TestCase):
    """signal_counts dict must be accurate."""

    def test_counts_by_type(self):
        signals_raw = [
            Signal(content="growth", source="Reuters", date="2025-01-01", signal_type="SUPPORTING"),
            Signal(content="growth", source="Reuters", date="2025-01-01", signal_type="SUPPORTING"),
            Signal(content="decline fall barrier", source="Bloomberg", date="2025-01-01", signal_type="OPPOSING"),
            Signal(content="unexpected collapse", source="FT", date="2025-01-01", signal_type="WILDCARD"),
        ]
        scored = [score_signal(s) for s in signals_raw]
        matrix = build_steeep_matrix(scored)
        self.assertEqual(matrix.signal_counts["SUPPORTING"], 2)
        self.assertEqual(matrix.signal_counts["OPPOSING"],   1)
        self.assertEqual(matrix.signal_counts["WILDCARD"],   1)
        self.assertEqual(matrix.signal_counts["total"],      4)

    def test_max_signals_count(self):
        signals = [_make_scored() for _ in range(50)]
        matrix = build_steeep_matrix(signals)
        self.assertEqual(matrix.signal_counts["total"], 50)


class TestMatrixBuilderModule(unittest.TestCase):
    """matrix_builder.py wrapper and utilities."""

    def test_build_matrix_returns_same_as_direct(self):
        signals = [_make_scored() for _ in range(10)]
        m1 = build_steeep_matrix(signals)
        m2 = build_matrix(signals)
        self.assertEqual(m1.hottest_cell, m2.hottest_cell)
        self.assertEqual(m1.net_direction, m2.net_direction)

    def test_get_matrix_summary_returns_string(self):
        signals = [_make_scored() for _ in range(5)]
        matrix = build_matrix(signals)
        summary = get_matrix_summary(matrix)
        self.assertIsInstance(summary, str)
        self.assertIn("Hot zone", summary)

    def test_get_dominant_zone_returns_dict(self):
        signals = [_make_scored() for _ in range(5)]
        matrix = build_matrix(signals)
        dom = get_dominant_zone(matrix)
        self.assertIn("hottest_cell", dom)
        self.assertIn("coverage_pct", dom)
        self.assertIsInstance(dom["coverage_pct"], int)


if __name__ == "__main__":
    unittest.main(verbosity=2)
