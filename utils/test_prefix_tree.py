import unittest
from utils.prefix_tree import *
from grammar_elements import *


class TestPrefixTree(unittest.TestCase):
    def test_simple(self):
        x = NonTerminal("X").and_with(Terminal("a")).or_with(Terminal("a")).and_with(Terminal("b"))
        tree = PrefixTree(x)
        tree.print_debug()
        alts = tree.get_alternatives_at(tree.get_tree_head('a'), 'a')

        self.assertEqual(alts, [[Terminal("a")], [Terminal("a"), Terminal("b")]])

    def test_moderate(self):
        x = NonTerminal("X").and_with(Terminal("a")).and_with(Terminal("b")) \
            .or_with(Terminal("a")).and_with(Terminal("b")).and_with(Terminal("c")) \
            .or_with(Terminal("a")).and_with(Terminal("b")).and_with(Terminal("d"))
        tree = PrefixTree(x)
        tree.print_debug()
        alts = tree.get_alternatives_at(tree.get_tree_head('a'), 'b')
        factored = tree.get_factored_out()

        # Alternatives prefixed ab, and the alternative ab itself
        alts.append([Terminal("a"), Terminal("b")])
        self.assertEqual(alts, factored['ab'])

    def test_hard(self):
        x = NonTerminal("X").and_with(Terminal("a")).and_with(Terminal("b")) \
            .or_with(Terminal("a")).and_with(Terminal("b")).and_with(Terminal("c")) \
            .or_with(Terminal("a")).and_with(Terminal("b")).and_with(Terminal("d")) \
            .or_with(Terminal("a")).and_with(Terminal("c")) \
            .or_with(Terminal("a")).and_with(Terminal("c")).and_with(Terminal("d")) \
            .or_with(Terminal("a")).and_with(Terminal("c")).and_with(Terminal("e")) \
            .or_with(Terminal("b")).and_with(Terminal("c")).and_with(Terminal("d")) \
            .or_with(Terminal("b")).and_with(Terminal("c")).and_with(Terminal("e"))

        tree = PrefixTree(x)
        tree.print_debug()
        alts_ab = tree.get_alternatives_at(tree.get_tree_head('a'), 'b')
        alts_ac = tree.get_alternatives_at(tree.get_tree_head('a'), 'c')
        alts_bc = tree.get_alternatives_at(tree.get_tree_head('b'), 'c')
        factored = tree.get_factored_out()

        # Alternatives prefixed ab, and the alternative ab itself
        alts_ab.append([Terminal("a"), Terminal("b")])
        alts_ac.append([Terminal("a"), Terminal("c")])
        self.assertEqual(alts_ab, factored['ab'])
        self.assertEqual(alts_ac, factored['ac'])
        self.assertEqual(alts_bc, factored['bc'])

    def test_lecture(self):
        x = NonTerminal("X") \
            .and_with(Terminal("a")).and_with(Terminal("b")).and_with(NonTerminal("B")) \
            .or_with(Terminal("a")).and_with(NonTerminal("B")) \
            .or_with(Terminal("c")).and_with(Terminal("d")).and_with(Terminal("g")) \
            .or_with(Terminal("c")).and_with(Terminal("d")).and_with(Terminal("e")).and_with(NonTerminal("B")) \
            .or_with(Terminal("c")).and_with(Terminal("d")).and_with(Terminal("f")).and_with(NonTerminal("B"))
        tree = PrefixTree(x)
        factored = tree.get_factored_out()

        self.assertTrue([Terminal("a"), NonTerminal("B")] in factored['a'])
        self.assertTrue([Terminal("a"), Terminal("b"), NonTerminal("B")] in factored['a'])

        self.assertTrue([Terminal("c"), Terminal("d"), Terminal("g")] in factored['cd'])
        self.assertTrue([Terminal("c"), Terminal("d"), Terminal("e"), NonTerminal("B")] in factored['cd'])
        self.assertTrue([Terminal("c"), Terminal("d"), Terminal("f"), NonTerminal("B")] in factored['cd'])


if __name__ == '__main__':
    unittest.main()
