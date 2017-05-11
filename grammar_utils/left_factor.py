from grammar_elements import *
from utils import prefix_tree


def left_factor(n: NonTerminal):
    """
    :param n: 
    :return: List of left factored non-terminals  
    """
    tree = prefix_tree.PrefixTree(n)
    out_non_terminal = NonTerminal(n.name)
    # Dict. of prefixes its list of non terminals
    factored = tree.get_factored_out()
    dash_count = 1
    for (i, key) in enumerate(factored.keys()):
        # Returns the prefix as a string and the factored elements, ex. (Given n: NonTerminal("Y"):
        # 'ab' -> [Terminal("a"), Terminal("b"), NonTerminal("X")], [Terminal("a"), Terminal("b"), Terminal("d")]
        rules = factored[key]

        # Returns the prefix elements: Terminal("a"), Terminal("b")
        (prefix_elements, rules) = __remove_prefix(key, rules)

        # Creates new non-terminals for factored out elements, ex.:
        # Y'  -> NonTerminal("X")
        # Y'' -> Terminal("d")
        non_terminal = __create_factored_non_terminal(n.name, rules, dash_count)
        dash_count += 1

        # Concatenates newly generated non-terminals with the factored elements
        # A' will become abY', Y'' will become abY''
        for element in prefix_elements:
            out_non_terminal.rule.append(element)

        out_non_terminal.rule.append(non_terminal)

        # Add an OR operation if there is another non-terminals present
        if i < len(factored) - 1:
            out_non_terminal.rule.append(OrOperation())

    return out_non_terminal


def __remove_prefix(prefix: str, rules: list):
    """
    Removes the factored prefix from the supplied grammar rules, as they're not removed 
    in the factoring operation
    :param prefix: 
    :param rules: 
    :return: Common terms that will remain in the source non-terminal
    """

    common_terms = []
    output_rules = []
    # Extract the prefix rule alone
    for i in range(0, len(prefix)):
        common_terms.append(rules[0][i])

    for rule in rules:
        rule_cp = rule[:]
        # Remove grammar elements from the rule as many as the prefix
        for i in range(0, len(prefix)):
            del rule_cp[0]

        # If all the rule is factored out, add an epsilon ex. 'ab', 'a' -> a('b'| \L)
        if len(rule_cp) == 0:
            rule_cp.append(Terminal.create_epsilon())

        output_rules.append(rule_cp)

    return common_terms, output_rules


def __create_factored_non_terminal(name: str, rules: list, dash_count: int):
    """
    Creates the new factored out non-terminals ex. Y', Y'', ...
    :param name: Name of the original non-terminal to be factored ie. Y
    :param rules: Grammar elements that were factored out
    :return: Newly factored non-terminals
    """
    nt = NonTerminal(name + (dash_count * '\''))
    for (i, rule) in enumerate(rules):
        nt.rule.append(rule)
        if i < len(rules) - 1:
            nt.rule.append(OrOperation())

    return nt
