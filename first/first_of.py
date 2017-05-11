from generic_helpers.decorators import memoize
from grammar_elements import *
from grammar_utils.get_nonterminal_children import get_non_terminal_children

# Don't cycle
__first_of_visited = []


def has_first_epsilon(el: GrammarElement):
    """
    Epsilon is added to first, iff the non terminal has and epsilon or all its children have an epsilon 
    """
    if el.type == ElementType.Terminal or el.type == ElementType.Epsilon:
        return False
    else:  # in case of a non terminal
        non_terminal_children = get_non_terminal_children(el)
        return el.has_epsilon() or (
            all([child.has_epsilon() for child in non_terminal_children]) and len(non_terminal_children) > 0)


@memoize
def __first_of(parent: GrammarElement):
    """
    Returns the first of this non terminal, without considering the epsilons
    """
    global __first_of_visited
    result = []
    if parent.type == ElementType.Terminal or parent.type == ElementType.Epsilon:  # case it is a terminal
        return [parent]

    for production in parent.productions:
        for (i, current_element) in enumerate(production):

            if i == 0 and current_element.type == ElementType.Terminal:
                result.append(current_element)

            if current_element in __first_of_visited:
                continue

            # Met a NonTerminal object in the first of a production,
            #  recursively check if `el` is in the `first` of the following
            elif (i == 0) and current_element.type == ElementType.NonTerminal:
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


def has_epsilon_in_list(list):
    return any([el.type == ElementType.Epsilon for el in list])


def get_first_of_list(list_of_non_terminals):
    if len(list_of_non_terminals) == 0: return []
    first = get_first(list_of_non_terminals[0])
    if has_epsilon_in_list(first):
        return first + get_first_of_list(list_of_non_terminals[1:])
    else:
        return first
