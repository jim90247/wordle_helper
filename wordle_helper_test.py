import unittest

from wordle_helper import WordFilter
from wordle_helper import Constraint


def match_target(constraints, target):
    word_filter = WordFilter()
    for word, verdict in constraints:
        constraint = Constraint(word, verdict)
        word_filter.add_constraint(constraint)
    return word_filter.match(target)


class TestWordFilter(unittest.TestCase):
    """The tests for WordFilter.
    """

    def test_empty(self):
        constraints = []

        self.assertTrue(match_target(constraints, "crane"))

    def test_nonrepeat_yellow(self):
        constraints = [("crane", [0, 0, 1, 0, 1])]

        self.assertTrue(match_target(constraints, "speak"))
        self.assertTrue(match_target(constraints, "xxxea"))
        self.assertFalse(match_target(constraints, "night"))
        self.assertFalse(match_target(constraints, "xxxxe"))

    def test_nonrepeat_green(self):
        constraints = [("crane", [0, 0, 2, 0, 1])]

        self.assertTrue(match_target(constraints, "least"))
        self.assertFalse(match_target(constraints, "clean"))
        self.assertFalse(match_target(constraints, "xxxxe"))

    def test_repeat_yellow(self):
        # 'e' only appear once
        constraints = [("creep", [0, 0, 1, 0, 0])]

        self.assertTrue(match_target(constraints, "exxxx"))
        self.assertFalse(match_target(constraints, "eexxx"))
        self.assertFalse(match_target(constraints, "xxexx"))
        self.assertFalse(match_target(constraints, "xxxex"))

    def test_repeat_green(self):
        # 'e' only appear once
        constraints = [("creep", [0, 0, 2, 0, 0])]

        self.assertTrue(match_target(constraints, "agent"))
        self.assertFalse(match_target(constraints, "exexx"))
        self.assertFalse(match_target(constraints, "xxxex"))

    def test_multiple(self):
        constraints = [("crane", [0, 0, 1, 0, 0]), ("atmos", [2, 0, 0, 1, 0])]

        self.assertTrue(match_target(constraints, "avoid"))
        self.assertFalse(match_target(constraints, "paths"))
        self.assertFalse(match_target(constraints, "adobe"))
