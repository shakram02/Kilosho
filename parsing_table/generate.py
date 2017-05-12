from first.first_of import get_first_of_list
from follow.follow_of import get_follow_table
from grammar_elements import Terminal
from grammar_reader.reader import from_file, get_terminals


def build_table(grammar_file_path='../grammar_reader/grammar_test.txt'):
    nonterminal_list = from_file(grammar_file_path)
    terminals_list = get_terminals(nonterminal_list)
    follow_table = get_follow_table(nonterminal_list)

    EPS = Terminal.create_epsilon()
    table = dict()

    for nonterminal in nonterminal_list:
        follows = follow_table[nonterminal]

        for production in nonterminal.productions:
            firsts = get_first_of_list(production)

            for terminal in firsts:
                add_production_to_table(table, nonterminal, terminal, production)

            if EPS in firsts:
                for terminal in follows:
                    add_production_to_table(table, nonterminal, terminal, production)

                if '$' in follows:
                    add_production_to_table(table, nonterminal, Terminal.create_dollar(), production)

    # check sync
    for nonterminal in nonterminal_list:
        follows_names = {x.name for x in follow_table[nonterminal]}
        temp_terminal = set(terminals_list[:])

        for production in nonterminal.productions:
            firsts = set(get_first_of_list(production))
            rest = temp_terminal - firsts

            for terminal in rest:
                if terminal in follows_names and terminal not in table[nonterminal.name]:
                    add_production_to_table(table, nonterminal, Terminal(terminal), 'sync')

    return table


def add_production_to_table(table, nonterminal, terminal, production):
    if nonterminal.name not in table:
        table[nonterminal.name] = dict()

    if terminal.name in table[nonterminal.name] and table[nonterminal.name][terminal.name] != production:
        print('Ambiguous Grammar')

    table[nonterminal.name][terminal.name] = production
