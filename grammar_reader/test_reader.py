import unittest
from grammar_reader import reader
from grammar_elements import ElementType


class TestFirst(unittest.TestCase):
    def test_from_string(self):
        result = reader.from_string("""A ::= B | c
        B ::= b | \L""")

        # assert that the number of rules found is correct
        self.assertEqual(len(result), 2)

        # assert first NonTerminal is found correctly
        self.assertEqual(result[0].type, ElementType.NonTerminal)
        self.assertEqual(result[0].rule[0].type, ElementType.NonTerminal)
        self.assertEqual(result[0].rule[1].type, ElementType.OrOperation)
        self.assertEqual(result[0].rule[2].type, ElementType.Terminal)

        # assert second NonTerminal is found correctly
        self.assertEqual(result[1].type, ElementType.NonTerminal)
        self.assertEqual(result[1].rule[0].type, ElementType.Terminal)
        self.assertEqual(result[1].rule[1].type, ElementType.OrOperation)
        self.assertEqual(result[1].rule[2].type, ElementType.Epsilon)
