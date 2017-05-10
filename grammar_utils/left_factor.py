from grammar_elements import *


def get_left_factored(n: NonTerminal):
    pass


def factor_out(n: NonTerminal):
    """
    Returns the common left factored elements in a given non terminal
    and also the un-factor-able elements
    :param n: Non terminal to factor out
    :return: Common elements in the non terminal
    """
    if len(n.rule) == 0:
        return None

    sub_elements = __setup_left_factoring(n)

    if len(sub_elements) == 1:
        return sub_elements[0]

    common = []
    uncommon = []
    prefix_dict = {}

    return common, uncommon


def get_sublist(x: list, y: list):
    """
    Finds a sublist in 2 lists 
    :return: List containing the intersection between 2 lists
    """
    common = []

    if len(x) < len(y):
        shorter_len = len(x)
    else:
        shorter_len = len(y)

    for i in range(0, shorter_len):
        if x[i] == y[i]:
            common.append(x[i])
        else:
            break

    return common


def __setup_left_factoring(n: NonTerminal):
    """
    Prepares for left-factoring, this is moved here for sanity
    :return: A length-sorted list of grammar sub-lists in the non terminal  
    """
    sub_elements = []
    # Add all the chunks of a non-terminal to a list
    # to prepare for left factoring
    for chunk in n:
        sub_elements.append(chunk)

    return sub_elements
