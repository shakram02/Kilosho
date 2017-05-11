from grammar_elements import *
import grammar_elements
from grammar_utils.left_factor import left_factor
import unittest


class TestLeftFactor(unittest.TestCase):
    def test_get_left_factor_simple(self):
        x = NonTerminal("X").and_with(Terminal("a")).and_with(Terminal("b")).or_with(Terminal("a"))
        factored = left_factor(x)
        self.assertTrue([Terminal("a"), NonTerminal("X'")] in factored)

        x = NonTerminal("X").and_with(NonTerminal("A")).and_with(Terminal("b")).or_with(NonTerminal("A"))
        factored = left_factor(x)
        self.assertTrue([NonTerminal("A"), NonTerminal("X'")] in factored)

    def test_get_left_factor_with_non_terminals(self):
        x = NonTerminal("X") \
            .and_with(Terminal("a")) \
            .or_with(Terminal("a")).and_with(NonTerminal("Z")) \
            .or_with(NonTerminal("Y"))

        factored = left_factor(x)
        self.assertTrue([Terminal("a"), NonTerminal("X'")] in factored)
        self.assertTrue([NonTerminal("Y")] in factored)

        # def test_fail_get_left_factor_with_non_terminals(self):
        #     x = NonTerminal("X") \
        #         .and_with(Terminal("a")).and_with(NonTerminal("Y")) \
        #         .or_with(Terminal("a")).and_with(NonTerminal("Y")) \
        #         .or_with(NonTerminal("Z"))  # Breaks the left factor
        #
        #     self.assertTrue(False)
