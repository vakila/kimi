# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import sys

def tokenize(string):
    '''Take a program as a string, return the tokenized program as a list of strings.

    >>> tokenize("(+ 1 2)")
    [('opening', None), ('symbol', '+'), ('literal', 1), ('literal', 2), ('closing', None)]

    >>> tokenize('(define x "some string")')
    [('opening', None), ('symbol', 'define'), ('symbol', 'x'), ('literal', 'some string'), ('closing', None)]

    >>> tokenize('(define x "some (string)")')
    [('opening', None), ('symbol', 'define'), ('symbol', 'x'), ('literal', 'some (string)'), ('closing', None)]

    >>> tokenize("(define square (lambda x (* x x)))")
    [('opening', None), ('symbol', 'define'), ('symbol', 'square'), ('opening', None), ('symbol', 'lambda'), ('symbol', 'x'), ('opening', None), ('symbol', '*'), ('symbol', 'x'), ('symbol', 'x'), ('closing', None), ('closing', None), ('closing', None)]

    '''

    special = ['(',')','"']
    whitespaces = [' ','\n','\t']
    tokens = []
    remaining = string#.strip()
    while remaining:
        this_char = remaining[0]
        if this_char in whitespaces:
            remaining = remaining[1:]
            continue
        if this_char in ["(", ")"]:
            # the token is this character
            if this_char == "(":
                token_type = 'opening'
            if this_char == ")":
                token_type = 'closing'
            token_value = None
            remaining = remaining[1:]#.strip()
        elif this_char == '"':
            # the token is everything until the next "
            endquote_index = remaining[1:].find('"')
            if endquote_index == -1:
                raise SyntaxError("Error in string syntax!")
            endquote_index += 1
            token_value = remaining[1:endquote_index]
            token_type = 'literal'
            remaining = remaining[endquote_index+1:]#.strip()
        else:
            # the token is everything until the next whitespace
            token_value = ""
            is_number = True
            while this_char not in special and this_char not in whitespaces:
                if not this_char.isdigit():
                    is_number = False
                token_value += this_char
                remaining = remaining[1:]
                this_char = remaining[0]
                if not this_char:
                    break
            if is_number:
                token_type = "literal"
                token_value = int(token_value)
            else:
                token_type = "symbol"
        tokens.append((token_type, token_value))
    return tokens

def parse(tokens):
    '''Take a list of tokens representing a program, return a tree representing the program's syntax.
    The tree is a nested dictionary, where each dictionary in the tree is an expression.

    Expressions as dictionaries:
    - All contain the key 'type'
    - Based on the value of 'type', the dictionary will also have other keys:
        - type 'apply' (function application) has keys 'operator' (value: expression) and 'arguments' (value: tuple of expressions)
        - type 'symbol' (variable or operator) has key 'name' (value: string representing the variable/operator)
        - type 'literal' (number, string, boolean, ...) has key 'value' (value: the literal)

    >>> parse(['(', '+', '1', '2', ')'])
    {'type': 'apply',
     'operator': {'type': 'symbol', 'name': '+'},
     'arguments': ({'type': 'literal', 'value': 1},
                   {'type': 'literal', 'value': 2}
                   )
     }

    >>> parse(['(', 'define', 'square', '(', 'lambda', 'x', '(', '*', 'x', 'x', ')', ')', ')'])
    {'type': 'apply',
     'operator': {'type': 'symbol', 'name': 'define'},
     'arguments': ({'type': 'symbol', 'name': 'square'},
                   {'type': 'apply',
                    'operator': {'type': 'symbol', 'name': 'lambda'},
                    'arguments': ({'type': 'symbol', 'name': 'x'},
                                  {'type': 'apply',
                                   'operator': {'type': 'symbol', 'name': '*'},
                                   'arguments': ({'type': 'symbol', 'name': 'x'},
                                                 {'type': 'symbol', 'name': 'x'}
                                                 )
                                    }
                                  )
                    }
                   )
     }

    '''
    if len(tokens) == 0:
        raise SyntaxError("Nothing to parse!")
    first = tokens.pop(0)
    if first == ')':
        raise SyntaxError("Unexpected ')'!")
    elif first == '(':
        #TODO recursively parse the rest of tokens
        pass
    else:
        return parse_atom(first)

def parse_atom(token):
    '''Takes an atomic expression and returns the expression as a dictionary.

    >>> parse_atom('2')
    {'type': 'literal', 'value': 1}

    >>> parse_atom('"some string"')
    {'type': 'literal', 'value': 'some string'}

    >>> parse_atom('+')
    {'type': 'symbol', 'name': '+'}
    '''
    token_type = 'literal'
    try:
        value = int(token)
    except:
        if '"' in token:
            # this lexical processing should be in the tokenizer
            if token.startswith('"') and token.endswith('"'):
                value = token.strip('"')
            else:
                raise SyntaxError("Incorrect string syntax:", token)
        else:
            token_type = 'symbol'


def evaluate(expression, environment):
    '''Take an expression and environment as dictionaries.
    Evaluate the expression in the context of the environment, and return the result.
    '''
    pass

def execute(program):
    '''Take a Kimi program as a string. Tokenize the program, parse the tokens into a tree,
    then evaluate the tree. Return the result, or an error message.'''
    return evaluate(parse(tokenize(program)))


if __name__ == "__main__":
    program = sys.argv[1]
    print(tokenize(program))
