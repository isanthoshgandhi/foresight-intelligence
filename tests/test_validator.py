"""
test_validator.py

Unit tests for input_validator.py
Tests all 5 rules, boundary conditions, and the 4 spec test inputs.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from input_validator import validate, format_rejection, ValidationResult


class TestRule1EntityReality(unittest.TestCase):
    """RULE 1 — Entity Reality"""

    def test_fictional_character_fails(self):
        result = validate("Will Harry Potter become a senator by 2030?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_1", result.rule_failed)

    def test_unnamed_friend_fails(self):
        result = validate("Will my friend become a millionaire by 2028?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_1", result.rule_failed)

    def test_real_person_passes(self):
        result = validate("Will Rahul Gandhi become PM of India by 2029?")
        self.assertTrue(result.valid)

    def test_company_passes(self):
        result = validate("Will Infosys reach a $100B valuation by 2030?")
        self.assertTrue(result.valid)


class TestRule2SystemExistence(unittest.TestCase):
    """RULE 2 — System Existence"""

    def test_president_of_mars_fails(self):
        result = validate("Will Divya become president of Mars?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_2", result.rule_failed)
        self.assertIn("Mars", result.failure_reason)

    def test_king_of_moon_fails(self):
        result = validate("Will Elon Musk become king of the Moon by 2040?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_2", result.rule_failed)

    def test_king_of_internet_fails(self):
        result = validate("Will Google become king of the internet by 2030?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_2", result.rule_failed)

    def test_real_pm_passes(self):
        result = validate("Will the Prime Minister of India announce new EV policy by 2026?")
        self.assertTrue(result.valid)

    def test_real_president_passes(self):
        result = validate("Will the President of the United States sign a climate bill by 2027?")
        self.assertTrue(result.valid)


class TestRule3TimeHorizon(unittest.TestCase):
    """RULE 3 — Time Horizon"""

    def test_million_years_fails(self):
        result = validate("Will humans survive on Earth for a million years?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_3", result.rule_failed)

    def test_post_human_fails(self):
        result = validate("Will post-human intelligence replace governments?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_3", result.rule_failed)

    def test_year_2100_fails(self):
        result = validate("Will India be the richest nation by 2100?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_3", result.rule_failed)

    def test_30_year_window_passes(self):
        result = validate("Will EVs dominate Indian cities by 2032?")
        self.assertTrue(result.valid)

    def test_near_term_passes(self):
        result = validate("Will India's GDP grow to $5 trillion by 2027?")
        self.assertTrue(result.valid)

    def test_year_2035_passes(self):
        result = validate("Will Indian B2B SaaS produce a $50B company by 2035?")
        self.assertTrue(result.valid)


class TestRule4SignalAvailability(unittest.TestCase):
    """RULE 4 — Signal Availability"""

    def test_private_internal_fails(self):
        result = validate("Will my company internal decision on pricing be correct by 2026?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_4", result.rule_failed)

    def test_public_company_passes(self):
        result = validate("Will Tata Motors achieve its EV sales target by 2026?")
        self.assertTrue(result.valid)

    def test_government_policy_passes(self):
        result = validate("Will India's PLI scheme drive $10B in electronics exports by 2026?")
        self.assertTrue(result.valid)


class TestRule5MinimumSpecificity(unittest.TestCase):
    """RULE 5 — Minimum Specificity"""

    def test_empty_query_fails(self):
        result = validate("")
        self.assertFalse(result.valid)

    def test_too_short_fails(self):
        result = validate("Will it happen?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_5", result.rule_failed)

    def test_what_will_happen_fails(self):
        result = validate("What will happen?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_5", result.rule_failed)

    def test_specific_query_passes(self):
        result = validate("Will the Indian rupee depreciate further against the dollar by 2026?")
        self.assertTrue(result.valid)


class TestSpecTestInputs(unittest.TestCase):
    """Run the 4 spec-defined test inputs."""

    def test_valid_1_rahul_gandhi(self):
        """Spec test 1: should be VALID"""
        result = validate("Will Rahul Gandhi become PM of India by 2029?")
        self.assertTrue(result.valid, f"Should be valid but got: {result}")
        self.assertTrue(result.proceed)
        self.assertIsNone(result.rule_failed)

    def test_valid_2_b2b_saas(self):
        """Spec test 2: should be VALID"""
        result = validate("Will Indian B2B SaaS produce a $50B company by 2035?")
        self.assertTrue(result.valid, f"Should be valid but got: {result}")

    def test_valid_3_ev_india(self):
        """Spec test 3: should be VALID"""
        result = validate("Will EVs dominate Indian cities by 2032?")
        self.assertTrue(result.valid, f"Should be valid but got: {result}")

    def test_invalid_4_divya_mars(self):
        """
        Spec test 4: should be INVALID
        Expected:
          Rule failed: RULE_2 — System Existence
          Reason: Mars has no political system.
        """
        result = validate("Will Divya become president of Mars?")
        self.assertFalse(result.valid)
        self.assertIn("RULE_2", result.rule_failed)
        self.assertIn("Mars", result.failure_reason)
        self.assertFalse(result.proceed)

    def test_invalid_4_rejection_format(self):
        """Spec test 4: rejection message format"""
        result = validate("Will Divya become president of Mars?")
        msg = format_rejection(result)
        self.assertIn("INVALID QUERY", msg)
        self.assertIn("RULE_2", msg)
        self.assertIn("Mars", msg)
        self.assertIn("Suggestion:", msg)


class TestValidationResult(unittest.TestCase):
    """Test the ValidationResult dataclass contract."""

    def test_valid_result_structure(self):
        result = validate("Will AI replace software engineers in India by 2030?")
        self.assertIsInstance(result, ValidationResult)
        self.assertIsInstance(result.valid, bool)
        self.assertIsInstance(result.proceed, bool)

    def test_invalid_result_has_rule_failed(self):
        result = validate("Will Divya become president of Mars?")
        self.assertFalse(result.valid)
        self.assertIsNotNone(result.rule_failed)
        self.assertIsNotNone(result.failure_reason)
        self.assertFalse(result.proceed)


if __name__ == "__main__":
    unittest.main(verbosity=2)
