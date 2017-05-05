from grammar_elements import *
from grammar_utils.get_nonterminal_children import get_non_terminal_children

# Don't cycle
__first_of_visited = []


def has_first_epsilon(el: NonTerminal):
    """
    Epsilon is added to first, iff the non terminal and all its children have an epsilon 
    """
    return el.has_epsilon() and all([child.has_epsilon() for child in get_non_terminal_children(el)])


def __first_of(parent: NonTerminal):
    """
    Returns the first of this non terminal, without considering the epsilons
    """
    global __first_of_visited
    result = []
    if len(parent.rule) == 0:
        return []  # Non terminal has no children

    for (i, current_element) in enumerate(parent.rule):

        if i == 0 and current_element.type == ElementType.Terminal:
            result.append(current_element)

        previous_element = parent.rule[i - 1]

        if current_element in __first_of_visited or current_element.type == ElementType.OrOperation:
            continue

        elif previous_element.type == ElementType.OrOperation \
                and current_element.type == ElementType.Terminal:
            result.append(current_element)

        # Met an OR operation, recursively check if `el` is in the `first` of the following
        elif (previous_element.type == ElementType.OrOperation or i == 0) \
                and current_element.type == ElementType.NonTerminal:
            # print("  ", current_element.name, "  ", current_element.type)
            # Append before diving, to avoid cycles
            __first_of_visited.append(current_element)
            for e in __first_of(current_element):
                result.append(e)

    return result


def get_first(el: NonTerminal):
    """
    Returns the `first` of a given non-terminal element
    :param el: 
    :return: 
    """
    result = __first_of(el)

    if has_first_epsilon(el):
        result.append(Terminal.create_epsilon())

    return result
