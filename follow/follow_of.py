from grammar_elements import Terminal, ElementType
from first.first_of import get_first_of_list, has_epsilon_in_list
from grammar_reader import reader
from pprint import pprint as pp


def remove_epsilon_from_list(list):
    return set([element for element in list if element.type != ElementType.Epsilon])


def get_follow_table(non_terminal_list):
    follow_table = {non_terminal_list[0]: {Terminal('$')}}
    # put default value in follow_table 
    for non_terminal in non_terminal_list[1:]:
        follow_table[non_terminal] = set()
    sum_of_follows = 1
    last_sum_of_follows = None
    # keep looping while no new follows are found
    while last_sum_of_follows != sum_of_follows:
        last_sum_of_follows = sum_of_follows
        for non_terminal in non_terminal_list:
            for production in non_terminal.productions:
                for i, element in enumerate(production):
                    if element.type == ElementType.NonTerminal:
                        first_of_rest = get_first_of_list(production[i + 1:])
                        added = remove_epsilon_from_list(first_of_rest)
                        follow_table[element] = follow_table[element].union(added)
                        if has_epsilon_in_list(first_of_rest) or len(added) == 0:
                            follow_table[element] = follow_table[element].union(follow_table[non_terminal])
        # update number of follows found
        sum_of_follows = sum_number_of_found_follows(follow_table)

    return follow_table


def sum_number_of_found_follows(follow_table):
    return sum([len(value) for _, value in follow_table.items()])


result = reader.from_string("""E ::= T E'
E' ::= + T E' | \L
T ::= F T'
T' ::= * F T' | \L
F ::= ( E ) | id""")
pp([(key.name, len(value)) for key, value in get_follow_table(result).items()])
