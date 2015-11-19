# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import operator as op
from errors import *

class Environment(dict):

    def __init__(self, name = "global", outer = None, variables=(), values=()):
        self.name = name
        self.outer = outer
        self.update(zip(variables, values))

    def get(self, key):
        if key in self:
            return self[key]
        elif self.outer == None:
            throw_error("name", "Undefined variable: " + key)
        else:
            return self.outer.get(key)

    def set(self, key, value):
        if key in self:
            throw_error("name", "Variable " + key + " already exists in " + self.name + " environment!")
        # else warn if exists in an outer env
        else:
            self[key] = value

def standard_env():
    '''Returns the standard environment as a dictionary of (variable: value) pairs
    '''
    env = Environment()

    add_booleans(env)
    add_arithmetic(env)
    add_logic(env)
    add_equality(env)
    add_comparison(env)
    add_strings(env)

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
            assert_or_complain(type(arg) == t,
                "TYPE ERROR! Invalid argument type: " + str(arg) + " is type " + type(arg).__name__ + ", expected type " + t.__name__ + ".")
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

def add_equality(env):
    def equals(a, b):
        if type(a) != type(b):
            return False
        else:
            return a == b
    env["="] = equals
    return env

def add_comparison(env):
    fns = [('>', op.gt),
           ('<', op.lt),
           ('>=', op.ge),
           ('<=', op.le)]
    for (symbol, fn) in fns:
        env[symbol] = verify_arg_type(fn, int)
    return env

def add_strings(env):
    return env
