import unittest

from parsing_table.generate import build_table


class TestTable(unittest.TestCase):
    def test_generation(self):
        # table = build_table('../parsing_table/test_grammar.txt')
        #
        # non_terminal = list(table.keys())[0]
        # assert (non_terminal.name == 'E')
        #
        # terminals = [x.name for x in table[non_terminal].keys()]
        # terminals.sort()
        # assert (terminals == ['$', '\L', 'a', 'b'])
        pass
