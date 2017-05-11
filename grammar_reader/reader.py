"""
Reads the grammar in text and returns Terminals and NonTerminal objects 
"""
import re

from grammar_elements import Terminal, NonTerminal, ElementType

OR_SYMBOL = '|'
EPSILON_SYMBOL = '\L'


def from_string(string):
    """
    :param string: a string that contains the syntax grammar rule definitions
    :return: a list of NonTerminal objects with their corresponding rules defined
    """
    non_terminals_dict = {}
    non_terminals_list = []
    # split by lines ending in '\n'  not followed by an OR_SYMBOL
    lines = re.split(r'\n', string)

    for line in lines:

        non_terminal_name, rule_string = line.replace('\n', ' ').split('::=')
        non_terminal_name = non_terminal_name.replace(' ', '')

        non_terminal = NonTerminal(non_terminal_name)

        rule_split = [element for element in rule_string.split(' ') if element != '']

        for i, grammar_element in enumerate(rule_split):
            # skip OR_SYMBOL
            if grammar_element == OR_SYMBOL:
                continue
            # turn the grammar_element string to a GrammarElement object
            else:
                if grammar_element == EPSILON_SYMBOL:
                    grammar_element = Terminal.create_epsilon()
                elif grammar_element[0].isupper():
                    grammar_element = NonTerminal(grammar_element)
                else:
                    grammar_element = Terminal(grammar_element)

            # add grammar_element to the non_terminal productions
            if rule_split[i - 1] == OR_SYMBOL:
                non_terminal.or_with(grammar_element)
            else:
                non_terminal.and_with(grammar_element)
        # add nonterminal to hash for faster retrieval
        non_terminals_dict[non_terminal.name] = non_terminal
        # append the found non_terminal to the resultant list
        non_terminals_list.append(non_terminal)

    # add correct references for NonTerminal objects in every productions
    for non_terminal in non_terminals_list:
        for production in non_terminal.productions:
            for i, element in enumerate(production):
                if element.type == ElementType.NonTerminal:
                    try:
                        production[i] = non_terminals_dict[element.name]
                    except:
                        # raise ValueError('Non terminal "' + element.name + '" is not defined.')
                        pass

    # return a list of the NonTerminal objects
    return non_terminals_list


def from_file(path):
    """
    :param path: a string of the path of the file containing the syntax grammar rule definitions
    :return: a list of NonTerminal objects with their corresponding rules defined 
    """
    content = open(path).read()
    return from_string(content)
