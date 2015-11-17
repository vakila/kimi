# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import sys

def tokenize(string):
    '''Take a program as a string, return the tokenized program as a list of strings.

    >>> tokenize("(+ 1 2)")
    ['(', '+', '1', '2', ')']

    >>> tokenize('(define x "some string")')
    ['(', 'define', 'x', '"some string"', ')']

    >>> tokenize("(define square (lambda x (* x x)))")
    ['(', 'define', 'square', '(', 'lambda', 'x', '(', '*', 'x', 'x', ')', ')', ')']
    '''
    string = string.replace("(", " ( ")
    string = string.replace(")", " ) ")
    tokens = string.split()
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
    # How is this going to know the difference between strings and symbols?
    pass


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
