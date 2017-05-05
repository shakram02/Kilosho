from grammar_elements import *

# For doing DFS without cycling
__non_terminal_visited = []


def __get_non_terminal_children(element: NonTerminal):
    """
    Recurse through the child elements
    """

    global __non_terminal_visited
    result = []

    for e in element.rule:

        if e.type != ElementType.NonTerminal or e in __non_terminal_visited:
            continue

        __non_terminal_visited.append(e)
        result.append(e)
        for item in __get_non_terminal_children(e):
            result.append(item)

    return result


def get_non_terminal_children(element: NonTerminal):
    """
    Gets all the child non terminals 
    """
    # Clear old memory
    global __non_terminal_visited
    __non_terminal_visited = []
    # Do DFS
    result = __get_non_terminal_children(element)

    return result
