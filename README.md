# Kimi
A lispy toy programming language that keeps it minimal,
and its interpreter in Python 3.

Created by [Anjana](https://github.com/vakila) at the [Recurse Center](https://www.recurse.com).

## Running programs
    $ python3 kimi.py "(+ 1 2)"
or
    $ python3 kimi.py my_program.kimi

## Running tests using doctest
    $ python3 -m doctest -v kimi.py

## Basic types
* Numbers are limited to integers (e.g. `1`, `43905302`)
* Strings must be wrapped in double quotes (e.g. `"my string"`). Escaped double quotes are not supported, but single quotes can be used (e.g. `"my \"quote\" string"` is not a valid string, but `"my 'quote' string"` is). Note that providing a program directly as a string on the command line may give you headaches with this.
* Booleans are `true` and `false`

## Planned features
* `lambda`
* Built-in functions
    * Arithmetic: `+`, `-`, `*`, `/`, `%`
    * Logic: `!`, `&`, `|`
    * Comparison: `=`, `>`, `<`, `>=`, `<=`
    * Strings: `concat`, `find`, `replace`, `substring`...?
* Function application
* Variable definition (names)
* Conditionals
* Lists (`empty`, `cons`, `first`, `rest`)

## Stay tuned!
