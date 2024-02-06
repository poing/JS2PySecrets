#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# func2str.py

from functools import wraps
import json


def function_to_string(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        args_str = ', '.join(repr(arg) for arg in args)
        kwargs_str = ', '.join(f'{key}={repr(value)}' for key, value in kwargs.items())
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))

        return f"{func.__name__}({all_args});"
    
    return wrapper

# Applying the decorator to functions
@function_to_string
def funcA(*args, **kwargs):
    pass

@function_to_string
def funcB(*args, **kwargs):
    pass 
    
funcC = function_to_string('blue')

# Testing
print(funcA("aa", "bb", 123, x=123))  # "funcA('aa', 'bb', 123, x=123)"
print(funcA('aa', 'bb', 123, x=123))   # "funcA('aa', 'bb', 123, x=123)"
print(funcA('aa', 'bb', 123, x=123))   # "funcA('aa', 'bb', 123, x=123)"

# Support and pass dict
print(funcB(["aa", "bb"], 123, x=123)) # 'funcB(["aa", "bb"], 123, x=123)'

foobar = "AAFF"

tasks = [
	funcA(foobar, 2, "that"),
	funcA(["some", "more", 2]),
	funcB("and something", "else", 2, plus=22),
	blue('hey'),
]

# Convert the Python dictionary to JSON
json_data = json.dumps(tasks, indent=None)

# Print or use the JSON data as needed
print(json_data)

