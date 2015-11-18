# Kimi language interpreter in Python 3
# Anjana Vakil
# http://www.github.com/vakila/kimi

def complain_and_die(message):
    print(message)
    quit()

def assert_or_complain(assertion, message):
    try:
        assert assertion
    except AssertionError:
        complain_and_die(message)
