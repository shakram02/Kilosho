import logging.handlers
import time

from generic_helpers.utils import get_nested_dict_values
from grammar_elements import GrammarElement
from grammar_reader.reader import from_file
from parsing_table.generate import build_table

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.handlers.TimedRotatingFileHandler("results/" + time.strftime("%Y-%m-%d") + ".log",
                                                    when="H", interval=12)
handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(handler)

input_stream = ['int', 'id', ';', 'id', 'assign', 'num', ';', 'if', '(', 'id', 'relop', 'num', ')', '{', 'id', 'assign',
                'num', ';', '}']


def get_next_input(input_stream):
    if len(input_stream) > 0:
        return input_stream[0], input_stream[1:]

    return '$', []


def trace(input_stream, grammar_file_path='../grammar_reader/grammar_test.txt'):
    productions = from_file(grammar_file_path)
    parsing_table = build_table(grammar_file_path)

    grammar_nonterminals = [x.name for x in productions]  # in order
    grammar_terminals = [y.name for x in get_nested_dict_values(parsing_table) for y in x if
                         isinstance(y, GrammarElement) and not y.name.isupper()]

    first_nonterminal = grammar_nonterminals[0]
    stack = ['$'] + [first_nonterminal]
    n_input, input_stream = get_next_input(input_stream)

    peek = stack[-1]
    while peek != '$':
        if peek in grammar_nonterminals:

            if n_input not in parsing_table[peek]:
                logger.error('Error: discarding "' + n_input + '"')
                n_input, input_stream = get_next_input(input_stream)
                continue

            production = parsing_table[peek][n_input]
            production = [x.name for x in production if isinstance(x, GrammarElement)]

            logger.debug(str(peek) + ' --> ' + ' '.join(production))

            if production == 'sync':
                logger.error('Error: "' + str(peek) + '" missing')
                stack.pop()
            else:
                stack.pop()
                for element in reversed(production):
                    if element != '\L':
                        stack.append(element)

        elif peek in grammar_terminals:
            if peek != n_input:  # matching error
                logger.error('Error: "' + peek + '" missing')
            else:
                logger.debug(str(peek) + ' --> ' + str(n_input))
                n_input, input_stream = get_next_input(input_stream)
            stack.pop()

        else:
            logger.error('Error: unknown symbol "' + n_input + '"')

        peek = stack[-1]

    stack.pop()
    return stack == input_stream


accept = trace(input_stream, '../grammar_reader/grammar_test_2.txt')

if accept:
    logger.debug('ACCEPT INPUT')
else:
    logger.debug('REFUSE INPUT')
