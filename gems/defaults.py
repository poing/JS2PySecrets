#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# defaults.py

import json
import js2pysecrets as secrets
from js2pysecrets.settings import Settings
import random


# Accessing Defaults
settings = Settings()
defaults = settings.get_defaults()
print(defaults.bits)  # Output: 8

# Updating Defaults
settings.update_defaults(bits=16)
defaults = settings.get_defaults()
print(defaults.bits)  # Output: 16

# Reverting to Default Values
settings.update_defaults()
defaults = settings.get_defaults()
print(defaults.bits)  # Output: 8 (reverted to the default value)

# Updating Defaults
settings.update_defaults(bits=16)
defaults = settings.get_defaults()
print(defaults.bits)  # Output: 16

# Reverting to Default Values
settings.reset_defaults()
defaults = settings.get_defaults()
print(defaults.bits)  # Output: 8 (reverted to the default value)

print(defaults.primitive_polynomials[12])

settings.update_defaults(bits=99)
print(defaults)

# from js2pysecrets import wrapper
# 
# 
# setup = []
# main = {'function': 'getConfig', 'args': []}
# tasks = {'tasks': [{'setup': setup, 'start': main}]}
# json_data = json.dumps(tasks, indent=None)
# print(wrapper(json_data))

# print(js2pysecrets.getConfig())
# print(js2pysecrets._reset())
# print(js2pysecrets.getConfig())

