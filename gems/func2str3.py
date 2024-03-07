#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# func2str3.py

"""
This script demonstrates making the JsFunction class work both as a callable and as a decorator. Excluding **kwargs in the output. Added test flag.
"""

class JsFunction:
    def __init__(self, func, test=False):
        self.func = func
        self.test = test

    def __call__(self, *args, test=False, **kwargs):
        def wrapped_func(*args, **kwargs):
            args_str = ', '.join(repr(arg) for arg in args)
            #kwargs_str = ', '.join(f'{key}={repr(value)}' 
            #	for key, value in kwargs.items())
            #all_args = ', '.join(filter(None, [args_str, kwargs_str]))

            return f"{self.func.__name__}({args_str})"
            
        data = ["init()"]
        if test or self.test:
        	data.append("setRNG('testRandom')")

        data.append(wrapped_func(*args, **kwargs) if args else self.func(*args, **kwargs))
        return data

    def __get__(self, instance, owner):
        return self if instance is None else types.MethodType(self, instance)

# Applied as a decorator
# Functional placeholder that uses the JS code, until the Python function is created
@JsFunction
def alpha(*args, **kwargs):
    pass

# Eventually independent python function will be created
def bravo():
    return "bravo('aa', 'bb', 123)"

# Create a alternately named instance of the JsFunction class that's callable
# Which is important for testing against python functions
testBravo = JsFunction(bravo, test=True)
regBravo = JsFunction(bravo)

"""
WARNING - WARNING - WARNING - WARNING - WARNING - WARNING
You cannot create an alternate instance using the JsFunction if it is already used.  Attempting to do so may lead to unexpected behavior.  For example, you cannot use testAlpha = JsFunction(alpha) if alpha() already has the JsFunction decorator applied.
WARNING - WARNING - WARNING - WARNING - WARNING - WARNING
"""

print(alpha("aa", "bb", 123, x=123))  # Returns: alpha('aa', 'bb', 123, x=123)
print(bravo()) # Returns: bravo('aa', 'bb', 123, x=123)
print(testBravo("aa", "bb", 123, x=123))  # Returns: bravo('aa', 'bb', 123, x=123)
print(regBravo("aa", "bb", 123, x=123))  # Returns: bravo('aa', 'bb', 123, x=123)

def string_comparison(str1, str2):
    if str1 == str2:
        return "Test Passed: Strings are equal"
    else:
        return "Test Failed: Strings are not equal"

print(string_comparison(alpha(123,'aaa'), testBravo(123,'aaa')))
print(string_comparison(bravo(), testBravo('aa', 'bb', 123, x=123)))
