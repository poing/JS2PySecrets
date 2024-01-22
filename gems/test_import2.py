#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test.py

import json
import js2pysecrets

# from js2pysecrets import wrapper
# 
# 
# setup = []
# main = {'function': 'getConfig', 'args': []}
# tasks = {'tasks': [{'setup': setup, 'start': main}]}
# json_data = json.dumps(tasks, indent=None)
# print(wrapper(json_data))

# print(js2pysecrets.share("ababab", 6, 3))
# print(js2pysecrets.getConfig())
# print(js2pysecrets._reset())
# print(js2pysecrets.getConfig())

# data = js2pysecrets.random(64)
# print(js2pysecrets.str2hex(data))
random = js2pysecrets.jsFunction('random', test=True)
print(random(32))
print(js2pysecrets.random(32))

