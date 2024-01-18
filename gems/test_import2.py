#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test.py

import json
from js2pysecrets import wrapper


setup = []
main = {'function': 'getConfig', 'args': []}
tasks = {'tasks': [{'setup': setup, 'start': main}]}
json_data = json.dumps(tasks, indent=None)
print(wrapper(json_data))