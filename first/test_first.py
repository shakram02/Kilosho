import unittest

from first.first_of import get_first
from grammar_elements import *


class TestFirst(unittest.TestCase):
    def test_first_simple(self):
        w = NonTerminal("W")
        x = NonTerminal("X")
        b = Terminal("b")
        a = Terminal("a")
        # x => b
        # w => a | x
        x.and_with(b)
        w.and_with(a).or_with(x)
        self.assertEqual(get_first(w), [a, b])

    def test_first_moderate(self):
        w = NonTerminal("W")
        x = NonTerminal("X")
        y = NonTerminal("Y")
        z = NonTerminal("Z")

        a = Terminal("a")
        b = Terminal("b")
        c = Terminal("c")
        d = Terminal("d")

        # X => b
        x.and_with(b)
        # Y => Z
        y.and_with(z)
        # Z => c | dc
        z.and_with(c).or_with(d).and_with(c)
        # W => a | X | Y
        w.and_with(a).or_with(x).or_with(y)
        self.assertEqual(get_first(w), [a, b, c, d])

    def test_first_with_epsilon(self):
        w = NonTerminal("W")
        x = NonTerminal("X")
        y = NonTerminal("Y")
        z = NonTerminal("Z")

        a = Terminal("a")
        b = Terminal("b")
        c = Terminal("c")
        d = Terminal("d")

        # X => b | (E
        x.and_with(b).or_with(Terminal.create_epsilon())
        # Y => Z | (E
        y.and_with(z).or_with(Terminal.create_epsilon())
        # Z => c | dc | (E
        z.and_with(c).or_with(d).and_with(c).or_with(Terminal.create_epsilon())
        # W => a | X | Y | (E
        w.and_with(a).or_with(x).or_with(y).or_with(Terminal.create_epsilon())
        self.assertEqual(get_first(w), [a, b, c, d, Terminal.create_epsilon()])

    def test_first_without_epsilon(self):
        w = NonTerminal("W")
        x = NonTerminal("X")
        y = NonTerminal("Y")
        z = NonTerminal("Z")

        a = Terminal("a")
        b = Terminal("b")
        c = Terminal("c")
        d = Terminal("d")

        # X => b | (E
        x.and_with(b).or_with(Terminal.create_epsilon())
        # Y => Z  <<=== No Epsilon here
        y.and_with(z)
        # Z => c | dc  <<=== No Epsilon here
        z.and_with(c).or_with(d).and_with(c)
        # W => a | X | Y
        w.and_with(a).or_with(x).or_with(y)
        self.assertEqual(get_first(w), [a, b, c, d])
