# Kimi
A lispy toy programming language that keeps it minimal,
and its interpreter in Python 3.

Created by [Anjana](https://github.com/vakila) at the [Recurse Center](https://www.recurse.com).

## Running programs
Run a program from a `.kimi` file:

    $ python3 kimi.py my_program.kimi

or type a program as a string on the command line (this may give you headaches)

    $ python3 kimi.py "(+ 1 2)"

## Running tests using doctest
    $ python3 -m doctest -v kimi.py

## Basics
* **Parentheses** are used to signal function calls, just like other lispy languages. Parentheses are not used for grouping, or any other purpose. For example, `(+ 1 2)` is a valid Kimi program, and `(+ (1) (2))` is not.
* **Numbers** are limited to integers (e.g. `1`, `-439`). Kimi assumes that anything that *can* be interpreted as an integer *is* an integer; for example, `2` and `+2` become `2`, and `-2` becomes `-2`. A number containing a decimal point (e.g. `2.5`) will *not* be considered an integer, but a **symbol** (see below).
* **Strings** must be wrapped in double quotes (e.g. `"my string"`). Kimi assumes anything surrounded by double quotes is a string. Escaped double quotes are not supported, but single quotes can be used (e.g. `"my \"quote\" string"` is not a valid string, but `"my 'quote' string"` is).
* **Booleans** are `true` and `false`
* Anything in your program that is not one of the above is considered a **symbol**.

## Names and scope
* Names can be assigned like so: `(define x 5)`.
* Any symbol (see above) is a valid name, as long as it does not already exist. For example, `x`, `123abc123`, and `--thing--` are valid names, but `define`, `-`, and `first` are not, since they already exist as built-in functions (see below).
* Just because something *can* be used as a name doesn't mean it *should*; for example `2.5` and `-2-4` are valid names (see above), but not very good ones!

## Built-in functions
* Arithmetic:
    * `+` (addition): `(+ 1 2) => 3`
    * `-` (subtraction): `(- 2 1) => 1`
    * `*` (multiplication): `(* 2 4) => 8`
    * `/` (floor division, as we have only integers): `(/ 6 2) => 3`, `(/ 7 2) => 3`
    * `%` (modulo): `(% 7 2) => 1`
* Logic:
    * `!` (not)
    * `&` (and)
    * `|` (inclusive or)

## Planned features
* `lambda`
* Built-in functions
    * Comparison: `=`, `>`, `<`, `>=`, `<=`
    * Strings: `concat`, `find`, `replace`, `substring`...?
* Function application
* Variable definition (names)
* Conditionals
* Lists (`empty`, `cons`, `first`, `rest`)

## Stay tuned!
