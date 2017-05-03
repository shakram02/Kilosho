import unittest
from grammar_elements import *
from first.first_of import has_first_epsilon


class TestDummyMod(unittest.TestCase):
    def test_has_epsilon_lv0(self):
        w = NonTerminal("W")
        # w -> a | (E
        w.and_with(Terminal("a")).or_with(Terminal.create_epsilon())
        self.assertTrue(has_first_epsilon(w))

    def test_has_epsilon_lv1(self):
        w = NonTerminal("W")
        x = NonTerminal("X")

        # x -> b | (E
        x.and_with(Terminal("b")).or_with(Terminal.create_epsilon())

        # w -> Xa | (E
        w.and_with(x).and_with(Terminal("a")).or_with(Terminal.create_epsilon())
        self.assertTrue(has_first_epsilon(w))
