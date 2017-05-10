import unittest
import pprint as pr
from utils.prefix_tree import *
from grammar_elements import *


class TestPrefixTree(unittest.TestCase):
    def test_simple(self):
        x = NonTerminal("X").and_with(Terminal("a")).or_with(Terminal("a")).and_with(Terminal("b"))
        tree = PrefixTree(x)
        tree.print_debug()
        alts = tree.get_alternatives_at(tree.get_tree_head('a'), 'a')

        self.assertEqual(alts, [[Terminal("a")], [Terminal("a"), Terminal("b")]])


if __name__ == '__main__':
    unittest.main()
