"""Tests fixed before the first plan measurement."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from measure_plan_readability import extract_prose, grade_from_counts


class ReadabilityTests(unittest.TestCase):
    def test_wrapped_paragraph(self):
        self.assertEqual(extract_prose("Keep the tools\nand start a new job.")[0],
                         "Keep the tools and start a new job.")

    def test_lists_are_separate_units(self):
        self.assertEqual(extract_prose("- [ ] Keep files safe\n- Test the copy.")[0],
                         "Keep files safe.\nTest the copy.")

    def test_exclusions_are_visible(self):
        prose, excluded = extract_prose("# Title\n| File | Hash |\n```\ncode()\n```\nUse `a.py` now.")
        self.assertEqual(prose, "Use now.")
        self.assertEqual(len(excluded), 6)

    def test_keep_explanations_and_criteria(self):
        prose, _ = extract_prose("**What & Why:** Keep all source files safe.\n\n**Acceptance criteria:**\n\n- [ ] Each link works.")
        self.assertEqual(prose, "Keep all source files safe.\nEach link works.")

    def test_links_keep_labels(self):
        self.assertEqual(extract_prose("Read the [source guide](guide.md).")[0],
                         "Read the source guide.")

    def test_formula_and_unrounded_boundary(self):
        self.assertAlmostEqual(grade_from_counts(100, 10, 150), 6.01)
        self.assertGreater(grade_from_counts(100, 10, 176), 9)

    def test_empty_counts_fail(self):
        with self.assertRaises(ValueError):
            grade_from_counts(0, 0, 0)

    def test_unclosed_fence_fails(self):
        with self.assertRaises(ValueError):
            extract_prose("Keep this.\n```\nhidden")


if __name__ == "__main__":
    unittest.main()
