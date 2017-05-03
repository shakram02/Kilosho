from grammar_elements import *


def first(el: GrammarElement):
    will_add = True
    has_epsilon = False

    if el.type == ElementType.Terminal:
        return el

    for e in el.rule:
        pass

    pass


def has_first_epsilon(el: GrammarElement):
    """
    Finds out if a production contains an epsilon for `first` function 
    """

    # The element is a terminal
    if el.type == ElementType.Terminal:
        return False

    # The element is an epsilon
    if el.type == ElementType.Epsilon:
        return True

    have_epsilon = False

    for e in el.rule:

        if e.type == ElementType.Epsilon:
            have_epsilon = True

        # Nothing to do for terminals
        if e.type != ElementType.NonTerminal:
            continue

        # Deep scanning of e if it's a non terminal
        have_epsilon = has_first_epsilon(e)

        # Shallow scanning of e, a child didn't have an epsilon
        # nothing more to be done return false
        if not e.has_epsilon() and have_epsilon is True:
            return False

        elif e.has_epsilon() and have_epsilon is False:
            have_epsilon = True

    return have_epsilon
