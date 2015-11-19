# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

import sys
from tokenizer import tokenize
from parser import parse
from evaluator import evaluate
from environments import standard_env
from errors import *

def execute(program):
    '''Take a Kimi program as a string. Tokenize the program, parse the tokens into a tree,
    then evaluate the tree. Return the result, or an error message.'''
    return evaluate(parse(tokenize(program)), standard_env())

def kimify(exp):
    '''Convert a Python object back into a Kimi-readable string.'''
    if exp == None:
        return "nil"
    elif type(exp) == bool:
        return {True: "true", False: "false"}[exp]
    elif type(exp) == int:
        return str(exp)
    elif type(exp) == str:
        return '"' + exp + '"'
    elif type(exp) == tuple:
        return "(list " + kimify_list(exp) + ")"

def kimify_list(tups):
    if tups[1] == None:
        return kimify(tups[0])
    else:
        return " ".join([kimify(tups[0]), kimify_list(tups[1])])


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
