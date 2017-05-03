from grammar_elements import *
import itertools

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

            # if len(sub_result) != 0:
            #     result.append(list(itertools.chain.from_iterable(sub_result)))
            # result.append(sub_result)

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

    # for item in :
    #     if type(item) is GrammarElement:
    #         result.append(item)
    #     elif type(item) is list and len(item) != 0:
    #         result.append(list(itertools.chain.from_iterable(item)))

    return result
