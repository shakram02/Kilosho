from grammar_elements import *
from grammar_utils.left_factor import get_left_factor
import unittest


class TestLeftFactor(unittest.TestCase):
    def test_get_left_factor_simple(self):
        x = NonTerminal("X").and_with(Terminal("a")).and_with(Terminal("b")).or_with(Terminal("a"))
        self.assertEqual(get_left_factor(x), [Terminal("a")])

    def test_get_left_factor_with_non_terminals(self):
        x = NonTerminal("X") \
            .and_with(Terminal("a")).and_with(NonTerminal("Y")) \
            .or_with(Terminal("a")).and_with(NonTerminal("Y"))

        self.assertEqual(get_left_factor(x), [Terminal("a"), NonTerminal("Y")])

    def test_fail_get_left_factor_with_non_terminals(self):
        x = NonTerminal("X") \
            .and_with(Terminal("a")).and_with(NonTerminal("Y")) \
            .or_with(Terminal("a")).and_with(NonTerminal("Y")) \
            .or_with(NonTerminal("Z"))  # Breaks the left factor

        self.assertEqual(get_left_factor(x), [Terminal("a"), NonTerminal("Y")])
