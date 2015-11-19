# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

from errors import *

def parse(tokens):
    '''Take a list of tokens representing a program, return a tree representing the program's syntax.
    The tree is a nested dictionary, where each dictionary in the tree is an expression.

    Expressions as dictionaries:
    - All contain the key 'type'
    - Based on the value of 'type', the dictionary will also have other keys:
        - type 'apply' (function application) has keys 'operator' (value: expression) and 'arguments' (value: tuple of expressions)
        - type 'symbol' (variable or operator) has key 'name' (value: string representing the variable/operator)
        - type 'literal' (number, string, boolean, ...) has key 'value' (value: the literal)

    >>> parse(tokenize("(+ 1 2)"))
    {'type': 'apply',
     'operator': {'type': 'symbol', 'value': '+'},
     'arguments': ({'type': 'literal', 'value': 1},
                   {'type': 'literal', 'value': 2})}

    '''
    # print("tokens:", tokens)
    if len(tokens) == 0:
        throw_error("syntax", "Nothing left to parse.")
    (token_type, token_value) = tokens.pop(0)
    if token_type == 'closing':
        throw_error("syntax", "Unexpected ')'.")
    elif token_type == 'opening':
        # print("OPENING")
        operator = parse(tokens)
        arguments = []
        while True:
            if not tokens:
                throw_error("syntax", "Unexpected end of program.")
            next_token = tokens[0]
            if next_token[0] == 'closing':
                # print("CLOSING")
                tokens.pop(0)
                # print("tokens:", tokens)
                break
            arguments.append(parse(tokens))
        arguments = tuple(arguments)
        return {'type': 'apply', 'operator': operator, 'arguments': arguments}
    else:
        return {'type': token_type, 'value': token_value}
