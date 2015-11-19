# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import evaluator as ev
from environments import Environment
from errors import *

def do(args, env):
    do_env = Environment(name="do", outer=env)
    if len(args) == 0:
        throw_error("syntax", "Incorrect use of (do ...): must take at least one argument.")
    result = None
    for a in args:
        result = ev.evaluate(a, do_env)
    return result

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
        return ev.evaluate(lbody, lenv)
    return anonymous

def define(args, env):
    if len(args) != 2:
        throw_error("syntax", "Incorrect use of (define ...): must take exactly two arguments.")
    assert_or_throw(args[0]['type'] == 'symbol', "type", "Incorrect use of (define ...): the variable must be a symbol.")
    variable = args[0]['value']
    env.set(variable, ev.evaluate(args[1], env))

def cond(args, env):
    if len(args) != 3:
        throw_error("syntax", "Incorrect use of (if ...): must take exactly three arguments (a test, a pass case, and a fail case).")
    test = ev.evaluate(args[0], env)
    if type(test) != bool:
        throw_error("type", "Incorrect use of (if ...): the test must evaluate to a boolean.")
    if test:
        return ev.evaluate(args[1], env)
    else:
        return ev.evaluate(args[2], env)

def special_forms():
    specials = dict()

    specials['do'] = do
    specials['lambda'] = lamb
    specials['define'] = define
    specials['if'] = cond

    return specials
