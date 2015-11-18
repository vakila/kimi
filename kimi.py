# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import sys
from environment import standard_env
from errors import *

def tokenize(string):
    '''Take a program as a string, return the tokenized program as a list of strings.

    >>> tokenize("-1")
    [('literal', -1)]

    >>> tokenize("(+ 1 2)")
    [('opening', None), ('symbol', '+'), ('literal', 1), ('literal', 2), ('closing', None)]
    '''
    assert_or_complain(string.count('(') == string.count(')'), "SYNTAX ERROR! Mismatching parentheses.")
    special = ['(',')','"']
    whitespaces = [' ','\n','\t']
    tokens = []
    remaining = string
    while remaining:
        this_char = remaining[0]
        if this_char in whitespaces:
            remaining = remaining[1:]
            continue
        if this_char in ["(", ")"]:
            # the token is this character
            if this_char == "(":
                token_type = 'opening'
                next_char = remaining[1]
                if next_char in special or next_char in whitespaces :
                    complain_and_die("SYNTAX ERROR! Incorrect parenthesis use: " + '"' + this_char + next_char + '". Opening parenthesis must be immediately followed by the name of a function.')
            if this_char == ")":
                token_type = 'closing'
            token_value = None
            remaining = remaining[1:]
        elif this_char == '"':
            # the token is everything until the next "
            endquote_index = remaining[1:].find('"')
            if endquote_index == -1:
                complain_and_die("SYNTAX ERROR! Improper string syntax.")
            endquote_index += 1
            token_value = remaining[1:endquote_index]
            token_type = 'literal'
            remaining = remaining[endquote_index+1:]
        else:
            # the token is everything until the next whitespace or special character
            token_value = ""
            while this_char not in special and this_char not in whitespaces:
                token_value += this_char
                remaining = remaining[1:]
                if not remaining:
                    break
                this_char = remaining[0]
            try:
                # anything that can be converted to int is a literal number
                token_value = int(token_value)
                token_type = "literal"
            except ValueError:
                # everything else is a symbol
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

    >>> parse(tokenize("(+ 1 2)"))
    {'type': 'apply',
     'operator': {'type': 'symbol', 'value': '+'},
     'arguments': ({'type': 'literal', 'value': 1},
                   {'type': 'literal', 'value': 2})}

    '''
    # print("tokens:", tokens)
    if len(tokens) == 0:
        complain_and_die("SYNTAX ERROR! Nothing left to parse.")
    (token_type, token_value) = tokens.pop(0)
    if token_type == 'closing':
        complain_and_die("SYNTAX ERROR! Unexpected ')'.")
    elif token_type == 'opening':
        # print("OPENING")
        operator = parse(tokens)
        arguments = []
        while True:
            if not tokens:
                complain_and_die("SYNTAX ERROR! Unexpected end of program.")
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


def special_forms():
    specials = dict()

    def do(args, env):
        if len(args) == 0:
            throw_error("syntax", "Incorrect use of (do ...): must take at least one argument.")
        result = None
        for a in args:
            result = evaluate(a, env)
        return result
    specials['do'] = do

    # def lamb(args, env):
    #     pass
    # specials['lambda'] = lamb

    # def define(args, env):
    #     pass
    # specials['define'] = define

    # def cond(args, env):
    #     pass
    # specials['if'] = cond

    return specials

SPECIALS = special_forms()

def get_special_if_exists(operator):
    if operator['type'] == 'symbol':
        name = operator['value']

    elif operator['type'] == 'apply':
        try:
            name = operator['operator']['value']
        except KeyError:
            throw_error("operator", "I don't know what to do with this operator: " + str(operator))

    if name in SPECIALS:
        return SPECIALS[name]
    else:
        return None

def evaluate(expression, environment):
    '''Take an expression and environment as dictionaries.
    Evaluate the expression in the context of the environment, and return the result.

    >>> evaluate(parse(tokenize("(+ 1 2)")), standard_env())
    3
    '''
    print("EVALUATING:", expression)
    expr_type = expression['type']
    print("EXPR_TYPE:", expr_type)
    if expr_type == 'literal':
        return expression['value']
    elif expr_type == 'symbol':
        symbol = expression['value']
        if symbol in environment:
            return environment[symbol]
        else:
            complain_and_die("NAME ERROR! Undefined variable: " + symbol)
            #TODO can we give more information about which environment we're in?
    elif expr_type == 'apply':
        operator = expression['operator']
        spec_form = get_special_if_exists(operator)
        if spec_form:
            return spec_form(expression['arguments'], environment)
        fn = evaluate(operator, environment)
        assert_or_complain(callable(fn), 'TYPE ERROR! Trying to call a non-function: ' + str(operator['value']) + '. Did you use parentheses correctly?')
        return fn(*[evaluate(arg, environment) for arg in expression['arguments']])
    else:
        complain_and_die("PARSING ERROR! Unexpected expression type: " + str(expression) + ".")

def execute(program):
    '''Take a Kimi program as a string. Tokenize the program, parse the tokens into a tree,
    then evaluate the tree. Return the result, or an error message.'''
    return evaluate(parse(tokenize(program)), standard_env())


if __name__ == "__main__":
    try:
        program = sys.argv[1]
    except:
        print("Usage:")
        print("$ python3 kimi.py my_program.kimi")
        print('$ python3 kimi.py "(+ 1 2)"')
    else:
        if program.endswith('.kimi'):
            with open(program, 'r') as f:
                program = f.read()
            print("Evaluating program:")
            print(program)
        print(execute(program))
