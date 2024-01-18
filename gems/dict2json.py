#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# dict2json.py

"""
This is a basic example of taking a Python dict and returning JSON.  

The goal is passing function names and argument groups in a nested JSON.

It's a work in progress where the assumption is, there will be a set of setup commands (that are likely static), followed by a dynamic command with var based arguments.
"""

import json

# key: value (the function & arguments)
setup = [
    {"function": "setRNG", "args": ["testRandom"]},
    {"function": "init", "args": [12, 'testRandom']}
]

# Dynamic Values
foo = ["1234abc", 6, 3]

# key: value (the function & dynamic arguments)
main = {"function": "share", "args": foo}

# Combine setup and main
tasks = [{"setup": setup, "start": main}]

# Convert the Python dictionary to JSON
json_data = json.dumps(tasks, indent=None)

# Print or use the JSON data as needed
print(json_data)
