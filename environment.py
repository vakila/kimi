# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

def standard_env():
    '''Returns the standard environment as a dictionary of (variable: value) pairs
    '''
    env = dict()

    env = add_booleans(env)

    env = add_arithmentic(env)

    env = add_logic(env)

    env = add_comparison(env)

    env = add_strings(env)

    return env


def add_booleans(env):
    env['true'] = True
    env['false'] = False
    return env

def add_arithmentic(env):
    return env

def add_logic(env):
    return env

def add_comparison(env):
    return env

def add_strings(env):
    return env
