# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

from errors import *

def tokenize(string):
    '''Take a program as a string, return the tokenized program as a list of strings.

    >>> tokenize("-1")
    [('literal', -1)]

    >>> tokenize("(+ 1 2)")
    [('opening', None), ('symbol', '+'), ('literal', 1), ('literal', 2), ('closing', None)]
    '''
    assert_or_throw(string.count('(') == string.count(')'), "syntax", "Mismatching parentheses!")
    assert_or_throw('(((' not in string, "syntax", 'Incorrect parenthesis use: "(((". Opening parenthesis must be immediately followed by a function.')
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
                try:
                    next_char = remaining[1]
                except IndexError:
                    throw_error("syntax", 'Incorrect parenthesis use: "(" at end of program.')
                else:
                    if next_char in [")", '"'] or next_char in whitespaces :
                        throw_error("syntax", "Incorrect parenthesis use: " + '"' + this_char + next_char + '". Opening parenthesis must be immediately followed by a function.')
            if this_char == ")":
                token_type = 'closing'
            token_value = None
            remaining = remaining[1:]
        elif this_char == '"':
            # the token is everything until the next "
            endquote_index = remaining[1:].find('"')
            if endquote_index == -1:
                throw_error("syntax", "Improper string syntax.")
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
