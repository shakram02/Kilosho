import unittest

from grammar_elements import *
from grammar_utils.get_nonterminal_children import get_non_terminal_children


class TestGetNonterminals(unittest.TestCase):
    def setUp(self):
        unittest.TestResult.buffer = True

    def test_lv0(self):
        s = NonTerminal("S")
        t = NonTerminal("T")
        u = NonTerminal("u")
        v = NonTerminal("V")

        # S => S | UV
        s.and_with(t).or_with(u).and_with(v)
        self.assertEqual(get_non_terminal_children(s), [t, u, v])

    def test_lv1(self):
        s = NonTerminal("S")
        t = NonTerminal("T")
        u = NonTerminal("u")
        v = NonTerminal("V")
        w = NonTerminal("W")
        x = NonTerminal("X")
        a = Terminal("A")

        w.and_with(a)
        w.and_with(x)  # W=> aX
        v.and_with(w)  # V => W
        u.and_with(v)  # U => V
        t.and_with(u)  # T => U
        s.and_with(t)  # S => T

        result = get_non_terminal_children(s)
        self.assertEqual(result, [t, u, v, w, x])
