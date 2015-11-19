# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import special_forms as sf
from environments import Environment
from errors import *

SPECIALS = sf.special_forms()

def evaluate(expression, environment):
    '''Take an expression and environment as dictionaries.
    Evaluate the expression in the context of the environment, and return the result.

    >>> evaluate(parse(tokenize("(+ 1 2)")), standard_env())
    3
    '''
    # print("EVALUATING:", expression)
    expr_type = expression['type']
    # print("EXPR_TYPE:", expr_type)
    if expr_type == 'literal':
        return expression['value']
    elif expr_type == 'symbol':
        symbol = expression['value']
        return environment.get(symbol)
    elif expr_type == 'apply':
        operator = expression['operator']
        if operator['type'] == 'symbol' and operator['value'] in SPECIALS:
            return SPECIALS[operator['value']](expression['arguments'], environment)
        fn = evaluate(operator, environment)
        assert_or_throw(callable(fn), "type", 'Trying to call a non-function. Did you use parentheses correctly?')
        return fn(*[evaluate(arg, environment) for arg in expression['arguments']])
    else:
        complain_and_die("PARSING ERROR! Unexpected expression type: " + str(expression) + ".")
