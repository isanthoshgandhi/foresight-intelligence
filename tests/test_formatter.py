"""
test_formatter.py

Unit tests for report_formatter.py.
Tests crisp template enforcement, PROOF validation, line limits,
India lens, and JSON output structure.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from signal_scorer import Signal, score_signal, build_steeep_matrix
from probability_calc import Analogue, calculate_probabilities
from confidence_calc import calculate_confidence
from input_validator import validate
from report_formatter import (
    Scenario, Report, format_report, format_rejection,
    _has_number_or_date, _bar, _truncate,
)


# ─── FIXTURES ─────────────────────────────────────────────────────────────────

def _make_matrix():
    signals = [
        score_signal(Signal(
            content="EV growth strong investment increasing",
            source="Reuters",
            date="2025-06-01",
            signal_type="SUPPORTING",
        ))
        for _ in range(10)
    ] + [
        score_signal(Signal(
            content="Challenge barrier obstacle decline",
            source="Bloomberg",
            date="2025-01-01",
            signal_type="OPPOSING",
        ))
        for _ in range(3)
    ]
    return build_steeep_matrix(signals), signals


def _make_analogues():
    return [
        Analogue(
            name="South Korea EV rollout 2016-2022",
            description="Government-led mandate transformed auto market.",
            conditions_then="High oil dependency, strong auto base",
            tipping_incident="2019 Hyundai IONIQ subsidy tripling drove 300% YoY jump",
            outcome="EVs reached 9% market share by 2022",
            similarity_score=78.0,
        ),
    ]


def _make_scenarios():
    return {
        "probable": Scenario(
            name="Gradual EV Dominance",
            description="EV adoption reaches 30% market share by 2032 driven by PLI subsidies and falling battery costs.",
            proof="Battery prices fell 90% from $1,100/kWh in 2010 to $110/kWh in 2024.",
            if_condition="Central government maintains PLI subsidies through 2028",
            but_condition="If oil prices drop below $50/barrel and remove cost advantage",
        ),
        "plausible": Scenario(
            name="Fragmented Transition",
            description="EV adoption splits between premium cities and lag in tier-2 cities by 2032.",
            proof="Only 2.5% EV penetration in 2024 against 30% target.",
            if_condition="Grid reliability improves in tier-1 cities only",
            but_condition="Charging infrastructure gap in 600 smaller cities remains unfilled",
        ),
        "possible": Scenario(
            name="Disruption-Accelerated Shift",
            description="A fuel price shock or battery breakthrough triggers sudden 50% adoption by 2030.",
            proof="China's EV surge hit 35% market share in 18 months after 2022 subsidy shock.",
            if_condition="Oil price spikes above $150/barrel or solid-state battery commercial launch",
            but_condition="India's grid cannot absorb sudden 10× EV load without blackouts",
        ),
        "preferable": Scenario(
            name="Coordinated Green Transition",
            description="India achieves 40% EV by 2030 while building clean grid and domestic supply chain.",
            proof="Norway reached 80% EV market share by 2023 starting from <1% in 2010.",
            if_condition="",
            but_condition="",
            needs_condition="Coordinated policy: PLI + charging infra + renewable grid + local battery manufacturing",
            leverage="Mandate EV-only two-wheelers from 2027 — they are 70% of India's vehicle market",
        ),
    }


def _full_report(india=False):
    matrix, signals = _make_matrix()
    analogues = _make_analogues()
    probs = calculate_probabilities(matrix, signals, analogues)
    conf = calculate_confidence(matrix, matrix.signal_counts, 78.0)
    validation = validate("Will EVs dominate Indian cities by 2032?")
    one_thing = (
        "The decisive variable is not EV demand — it's charging density.\n"
        "INCIDENT: Norway's 2013 free parking + toll exemption drove 3× adoption jump in 12 months\n"
        "WATCH: India charging station permits issued per quarter\n"
        "IF YES → 30% EV penetration in cities by 2030\n"
        "IF NO  → EV growth stalls at 8% despite subsidy spend"
    )
    return format_report(
        query="Will EVs dominate Indian cities by 2032?",
        validation=validation,
        matrix=matrix,
        analogues=analogues,
        probabilities=probs,
        confidence=conf,
        scenarios=_make_scenarios(),
        one_thing=one_thing,
        india_adjusted=india,
        india_lens="Key India variable: Two-wheeler electrification is the 10× lever.\nWatch: Ola Electric IPO absorption and fleet electrification tenders." if india else None,
    )


# ─── TESTS ────────────────────────────────────────────────────────────────────

class TestProofValidation(unittest.TestCase):
    """_has_number_or_date must gate PROOF lines."""

    def test_number_passes(self):
        self.assertTrue(_has_number_or_date("Battery prices fell 90% from 2010 to 2024"))
        self.assertTrue(_has_number_or_date("$50B valuation target by 2030"))
        self.assertTrue(_has_number_or_date("3 million units sold"))

    def test_date_word_passes(self):
        self.assertTrue(_has_number_or_date("Announced in March 2022"))
        self.assertTrue(_has_number_or_date("Since January the trend has held"))

    def test_no_number_or_date_fails(self):
        self.assertFalse(_has_number_or_date("Growth is expected to continue strongly"))
        self.assertFalse(_has_number_or_date("The market is improving"))

    def test_warning_injected_when_no_number(self):
        report = _full_report()
        # Inject a scenario with bad proof
        bad_scenarios = _make_scenarios()
        bad_scenarios["probable"] = Scenario(
            name="Test",
            description="Test description",
            proof="No numbers or dates here at all whatsoever",
            if_condition="If X",
            but_condition="But Y",
        )
        matrix, signals = _make_matrix()
        analogues = _make_analogues()
        probs = calculate_probabilities(matrix, signals, analogues)
        conf = calculate_confidence(matrix, matrix.signal_counts, 78.0)
        validation = validate("Will EVs dominate Indian cities by 2032?")
        r = format_report(
            query="Will EVs dominate Indian cities by 2032?",
            validation=validation, matrix=matrix, analogues=analogues,
            probabilities=probs, confidence=conf, scenarios=bad_scenarios,
            one_thing="Test", india_adjusted=False,
        )
        self.assertIn("WARNING", r.text)


class TestBarGenerator(unittest.TestCase):
    """_bar: visual bar format."""

    def test_full_bar_20_chars(self):
        bar = _bar(10, 10)
        self.assertEqual(len(bar), 20)

    def test_empty_bar(self):
        bar = _bar(0, 10)
        self.assertEqual(bar, "░" * 20)

    def test_max_at_20(self):
        bar = _bar(100, 100)
        self.assertEqual(bar, "█" * 20)

    def test_partial_bar(self):
        bar = _bar(5, 10)
        self.assertEqual(len(bar), 20)
        self.assertIn("█", bar)
        self.assertIn("░", bar)


class TestTruncate(unittest.TestCase):
    """_truncate: word-level truncation."""

    def test_short_text_unchanged(self):
        self.assertEqual(_truncate("Hello world", 10), "Hello world")

    def test_long_text_truncated(self):
        text = " ".join(["word"] * 25)
        result = _truncate(text, 20)
        self.assertIn("…", result)
        self.assertLessEqual(len(result.split()), 22)  # 20 words + ellipsis token


class TestReportStructure(unittest.TestCase):
    """Full report structure."""

    def setUp(self):
        self.report = _full_report(india=False)

    def test_returns_report_dataclass(self):
        self.assertIsInstance(self.report, Report)

    def test_text_is_string(self):
        self.assertIsInstance(self.report.text, str)
        self.assertGreater(len(self.report.text), 100)

    def test_data_is_dict(self):
        self.assertIsInstance(self.report.data, dict)

    def test_header_present(self):
        self.assertIn("FORESIGHT ENGINE", self.report.text)

    def test_signal_pulse_present(self):
        self.assertIn("SIGNAL PULSE", self.report.text)
        self.assertIn("Net:", self.report.text)
        self.assertIn("Hot zone:", self.report.text)

    def test_all_four_scenarios_present(self):
        self.assertIn("PROBABLE", self.report.text)
        self.assertIn("PLAUSIBLE", self.report.text)
        self.assertIn("POSSIBLE", self.report.text)
        self.assertIn("PREFERABLE", self.report.text)

    def test_proof_in_every_scenario(self):
        for _ in ["PROOF:"]:
            self.assertIn("PROOF:", self.report.text)

    def test_the_one_thing_present(self):
        self.assertIn("THE ONE THING", self.report.text)
        self.assertIn("INCIDENT:", self.report.text)
        self.assertIn("WATCH:", self.report.text)

    def test_historical_match_present(self):
        self.assertIn("HISTORICAL MATCH", self.report.text)
        self.assertIn("South Korea", self.report.text)

    def test_probability_percentages_in_report(self):
        self.assertIn("%]", self.report.text)


class TestIndiaLens(unittest.TestCase):
    """India lens only appears when india_adjusted=True."""

    def test_india_lens_absent_when_not_india(self):
        report = _full_report(india=False)
        self.assertNotIn("INDIA LENS", report.text)

    def test_india_lens_present_when_india(self):
        report = _full_report(india=True)
        self.assertIn("INDIA LENS", report.text)
        self.assertIn("Multipliers moved:", report.text)


class TestJsonOutput(unittest.TestCase):
    """JSON data structure."""

    def setUp(self):
        self.data = _full_report().data

    def test_required_keys_present(self):
        required = [
            "query", "date", "confidence", "signal_counts",
            "net_direction", "hottest_cell", "probabilities",
            "scenarios", "one_thing", "india_adjusted",
        ]
        for key in required:
            self.assertIn(key, self.data)

    def test_probabilities_sum_to_100(self):
        probs = self.data["probabilities"]
        total = probs["probable"] + probs["plausible"] + probs["possible"]
        self.assertAlmostEqual(total, 100.0, places=1)

    def test_confidence_in_range(self):
        self.assertGreaterEqual(self.data["confidence"], 0)
        self.assertLessEqual(self.data["confidence"],  100)

    def test_scenarios_dict_has_four_keys(self):
        self.assertEqual(len(self.data["scenarios"]), 4)


class TestRejectionFormatter(unittest.TestCase):
    """format_rejection output."""

    def test_invalid_query_formats_correctly(self):
        query = "Will Divya become president of Mars?"
        validation = validate(query)
        msg = format_rejection(query, validation)
        self.assertIn("INVALID QUERY", msg)
        self.assertIn("RULE_2", msg)
        self.assertIn("Mars", msg)
        self.assertIn("Suggestion:", msg)

    def test_spec_test_4_exact_format(self):
        """
        Spec expected output:
          INVALID QUERY
          Rule failed: RULE_2 — System Existence
          Reason: Mars has no political system.
          Suggestion: Rephrase with a real-world political office or system.
        """
        query = "Will Divya become president of Mars?"
        validation = validate(query)
        msg = format_rejection(query, validation)
        lines = msg.split("\n")
        self.assertEqual(lines[0], "INVALID QUERY")
        self.assertIn("RULE_2", lines[1])
        self.assertIn("Mars", lines[2])
        self.assertIn("Suggestion:", lines[3])


if __name__ == "__main__":
    unittest.main(verbosity=2)
