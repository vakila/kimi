# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import operator as op

def standard_env():
    '''Returns the standard environment as a dictionary of (variable: value) pairs
    '''
    env = dict()

    env = add_booleans(env)

    env = add_arithmetic(env)

    env = add_logic(env)

    env = add_comparison(env)

    env = add_strings(env)

    return env


def add_booleans(env):
    env['true'] = True
    env['false'] = False
    return env

def verify_arg_type(fn, t):
    '''Function wrapper that makes function fn only accept arguments of type t.
    Throws an error if non-t arguments are passed to fn, otherwise calls fn on the arguments.
    '''
    def verifier(*args):
        for arg in args:
            if type(arg) != t:
                raise TypeError("Invalid argument type! " + str(arg) + " is type " + type(arg).__name__ + ", expected type " + t.__name__ + ".")
        return fn(*args)
    return verifier

def add_arithmetic(env):
    fns = [('+', op.add),
           ('-', op.sub),
           ('*', op.mul),
           ('/', op.floordiv),
           ('%', op.mod)]
    for (symbol, fn) in fns:
        env[symbol] = verify_arg_type(fn, int)
    return env

def add_logic(env):
    fns = [('&', lambda a,b: a and b),
           ('|', lambda a,b: a or b),
           ('!', lambda a: not a)]
    for (symbol, fn) in fns:
        env[symbol] = verify_arg_type(fn, bool)
    return env

def add_comparison(env):
    return env

def add_strings(env):
    return env
