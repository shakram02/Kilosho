from grammar_elements import *

__current_factor = []


def left_factor(n: NonTerminal):
    if len(n.rule) == 0:
        return None

    sub_elements = []

    global __current_factor
    __current_factor = []

    # Add all the chunks of a non-terminal to a list
    # to prepare for left factoring
    for chunk in n:
        sub_elements.append(chunk)

    if len(sub_elements) == 1:
        return sub_elements[0]

    sub_elements.sort(key=lambda x: len(x))

    key_chunk = sub_elements[0]
    common = get_sublist(key_chunk, sub_elements[1])

    for i in range(2, len(sub_elements)):
        # For all the other elements after the first one
        new_common = get_sublist(common, sub_elements[i])

        if len(common) == 0:
            return None

        if len(new_common) < len(common):
            common = new_common

    return common


def get_sublist(x: list, y: list):
    return []
