from grammar_elements import *
import unittest


class GrammarTests(unittest.TestCase):
    """
    About testing
    - All modules should be importable from the top module to be tested, ie. include __init__.py
    
    https://docs.python.org/3/library/unittest.html
    https://www.blog.pythonlibrary.org/2016/07/07/python-3-testing-an-intro-to-unittest/
    """

    def test_and(self):
        a = Terminal("a")
        b = Terminal("b")
        x = NonTerminal("X")
        # x -> a | b
        x.and_with(a).or_with(b)
        self.assertEqual(len(x.rule), 3, "Rule element count mismatch, "
                                         "should be 3: 2 terminals and 1 operator")

    def test_iterator(self):
        x = NonTerminal("X").and_with(Terminal("a")).or_with(Terminal("b"))

        iter_parts = []
        for item in x:
            for el in item:
                iter_parts.append(el)

        self.assertEqual(iter_parts, [Terminal("a"), Terminal("b")])

    def test_iterator_moderate(self):
        x = NonTerminal("X").and_with(Terminal("a")).and_with(NonTerminal("Y")).or_with(Terminal("b"))

        iter_parts = []

        for item in x:
            # Flatten for assert comparison
            for el in item:
                iter_parts.append(el)

        self.assertEqual(iter_parts, [Terminal("a"), NonTerminal("Y"), Terminal("b")])

    def test_iterator_above_moderate(self):
        x = NonTerminal("X").and_with(Terminal("a")).and_with(NonTerminal("Y")) \
            .or_with(Terminal("b")).and_with(Terminal("d")) \
            .or_with(NonTerminal("Y"))

        iter_parts = []

        for item in x:
            for el in item:
                iter_parts.append(el)

        self.assertEqual(iter_parts,
                         [Terminal("a"), NonTerminal("Y"),
                          Terminal("b"), Terminal("d"),
                          NonTerminal("Y")])
