#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test_func.py

from test_inject import TESTER

#TESTER = True  # Define the TESTER variable

def forTesting(str1='What', str2='Now'):
    result = str1 + ' ' + str2
    if TESTER:
    	return "blaa blaa"
    else:
    	return result

# A decorator function to inject behavior
def inject_behavior(original_function):
    def wrapper(*args, **kwargs):
        if TESTER:
            kwargs['str2'] = "Developer"
        return original_function(*args, **kwargs)
    return wrapper

# Wrap the forTesting function with the inject_behavior decorator
#forTesting = inject_behavior(forTesting)
