#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#

import random

def base_value(value, default=6):
    if value is None:
        return default
    elif value is False:
        return None
    elif callable(value):
        return value()
    elif isinstance(value, int):
        return value
    elif isinstance(value, str):
        return value
    else:
        return None

print(base_value(None))
print(base_value(lambda: 10*10))
print(base_value(33))
print(base_value(0))
print(base_value(-33))
print(base_value('hello'))
print(base_value(False))


def low_random(value, standard=6):
    return int(random.triangular(standard, value, standard))

print(low_random(7))
print(low_random(20))
print(low_random(60))
print(low_random(10000))
print(low_random(100000))