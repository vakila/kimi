# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import sys
from environment import Environment, standard_env
from tokenize import tokenize
from parse import parse
from errors import *

def special_forms():
    specials = dict()

    def do(args, env):
        do_env = Environment(name="do", outer=env)
        if len(args) == 0:
            throw_error("syntax", "Incorrect use of (do ...): must take at least one argument.")
        result = None
        for a in args:
            result = evaluate(a, do_env)
        return result
    specials['do'] = do

    def lamb(args, env):
        # print("\n")
        # print("args (" + str(len(args)) + "):", args)
        # print("env: ", env.name)
        if len(args) < 2:
            throw_error("syntax", "Incorrect use of (lambda ...): must take at least two arguments (at least one variable and a body).")
        largs = args[:-1]
        lbody = args[-1]
        # print("largs (" + str(len(largs)) + "):", largs)
        for l in largs:
            assert_or_throw(l['type'] == 'symbol', "syntax", "Incorrect use of (lambda ...): the anonymous function's variables must be symbols.")
        largs = tuple(la['value'] for la in largs)
        # print("lbody:", lbody)
        def anonymous(*arguments):
            # print("inside anonymous function")
            # print("arguments(" + str(len(arguments)) + "):", arguments)
            if len(arguments) != len(largs):
                throw_error("syntax", "This function takes " + str(len(largs)) + " arguments (" + str(len(arguments)) + " provided).")
            lenv = Environment(name="anon_fn", outer=env, variables=largs, values=arguments)
            return evaluate(lbody, lenv)
        return anonymous
    specials['lambda'] = lamb

    def define(args, env):
        if len(args) != 2:
            throw_error("syntax", "Incorrect use of (define ...): must take exactly two arguments.")
        assert_or_throw(args[0]['type'] == 'symbol', "type", "Incorrect use of (define ...): the variable must be a symbol.")
        variable = args[0]['value']
        env.set(variable, evaluate(args[1], env))
    specials['define'] = define

    def cond(args, env):
        if len(args) != 3:
            throw_error("syntax", "Incorrect use of (if ...): must take exactly three arguments (a test, a pass case, and a fail case).")
        test = evaluate(args[0], env)
        if type(test) != bool:
            throw_error("type", "Incorrect use of (if ...): the test must evaluate to a boolean.")
        if test:
            return evaluate(args[1], env)
        else:
            return evaluate(args[2], env)
    specials['if'] = cond

    return specials

SPECIALS = special_forms()

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
