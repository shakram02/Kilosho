import unittest
from grammar_elements import *
from first.first_of import has_first_epsilon


class TestHasEpsilon(unittest.TestCase):
    def test_eps_flat_positive(self):
        """
        - Flat, has epsilon
        - Flat, no epsilon
        :return: 
        """
        w = NonTerminal("W")
        # w -> a | (E
        w.and_with(Terminal("a")).or_with(Terminal.create_epsilon())
        self.assertTrue(has_first_epsilon(w))

        x = NonTerminal("X")
        x.and_with(x)
        self.assertFalse(has_first_epsilon(x))

    def test_eps_flat_negative(self):
        w = NonTerminal("W")
        # w -> a
        w.and_with(Terminal("a"))
        x = has_first_epsilon(w)
        self.assertFalse(x)

    def test_eps_chained_positive(self):
        """
        - Chained, has epsilon
        """
        w = NonTerminal("W")
        x = NonTerminal("X")

        # x -> b | (E
        x.and_with(Terminal("b")).or_with(Terminal.create_epsilon())

        # w -> Xa | (E
        w.and_with(x).and_with(Terminal("a")).or_with(Terminal.create_epsilon())
        self.assertTrue(has_first_epsilon(w))

    def test_eps_chained_negative(self):
        """
        - Chained, no epsilon
        """
        w = NonTerminal("W")
        x = NonTerminal("X")
        x.and_with(w)
        # X => W
        self.assertFalse(has_first_epsilon(x))
