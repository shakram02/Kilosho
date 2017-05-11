from first.first_of import *
from follow.follow_of import get_follow_table
from grammar_reader.reader import from_file


def build_table(grammar_file_path='../grammar_reader/grammar_test.txt'):
    nonterminal_list = from_file(grammar_file_path)
    follow_table = get_follow_table(nonterminal_list)

    EPS = Terminal.create_epsilon()
    table = dict()

    for nonterminal in nonterminal_list:
        list_of_sub_productions = nonterminal.productions
        follows = follow_table[nonterminal]

        for production in list_of_sub_productions:
            # firsts = get_first(production)
            firsts = get_first_of_list(production)

            for terminal in firsts:
                add_production_to_table(table, nonterminal, terminal, production)

            if EPS in firsts:
                for terminal in follows:
                    add_production_to_table(table, nonterminal, terminal, production)

                if '$' in follows:
                    add_production_to_table(table, nonterminal, '$', production)

    return table


def add_production_to_table(table, nonterminal, terminal, production):
    if nonterminal not in table:
        table[nonterminal] = dict()

    if terminal in table[nonterminal]:
        print('Ambiguous Grammar')

    table[nonterminal][terminal] = production
