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

def repl():
    '''An interactive Read-Evaluate-Print Loop that takes in Kimi code from a prompt and evaluates it.'''
    quit_commands = ["exit", "quit", "q"]
    print("Welcome to Kimi!")
    print("See the README (https://github.com/vakila/kimi) for information about Kimi.")
    print('To exit the interpreter, type "' + '" or "'.join(quit_commands) + '".')
    prompt = 'kimi> '
    global_env = standard_env()
    while True:
        command = input(prompt)
        if command in quit_commands:
            return "Goodbye!"
        val = evaluate(parse(tokenize(command)), global_env)
        print(kimify(val))

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
    if len(sys.argv) == 1:
        repl()
        #activate repl
    elif len(sys.argv) == 2:
        program = sys.argv[1]
        if program.endswith('.kimi'):
            with open(program, 'r') as f:
                program = f.read()
            # print("Evaluating program:")
            # print(program)
            # print("\nResult:")
        print(kimify(execute(program)))
    else:
        print("Usage:")
        print("Activate the interactive interpreter (REPL): $ python3 kimi.py")
        print("Evaluate a Kimi program in an external file: $ python3 kimi.py my_program.kimi")
        print('Evaluate a simple Kimi program as a string:  $ python3 kimi.py "(+ 1 2)"')
