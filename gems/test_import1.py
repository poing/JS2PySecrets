#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test.py

import json
from js2pysecrets import wrapper


# Example usage
# Setup commands
setup = [
    {'function': 'setRNG', 'args': ['testRandom']},
]

# Dynamic Values
foo = ['1234abc', 6, 3]

# Main function
main = {'function': 'share', 'args': foo}

# Combine setup and main
tasks = {'tasks': [{'setup': setup, 'start': main}]}

# Convert the Python dictionary to JSON
json_data = json.dumps(tasks, indent=None)
#print(json_data)

doit = wrapper(json_data)
print(doit)
