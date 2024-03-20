#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# defaults.py

import json
import js2pysecrets.node as node

import random

# This does not work

import js2pysecrets as secrets
from js2pysecrets.settings import Settings
settings = Settings()



#config = settings.get_config()
#print(secrets.isSetRNG())

secrets.setRNG('hello')
config = settings.get_config()
#print(secrets.isSetRNG())

#settings.update_defaults(rng=99)
#secrets.setRNG(999)
#config = settings.get_config()

#print(config.rng)
#print(secrets.isSetRNG())



secrets.setRNG(lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits))
config = settings.get_config()

print(settings.rng(8))
#config.rng(8)

# pre_gen_padding = "0" * 1024  # Pre-generate a string of 1024 '0's


print(secrets.getConfig())

data = node.getConfig()
print(data)


foo = secrets.str2hex('hello world', 2)
bar = node.str2hex('hello world', 2)

print(secrets.hex2str(bar))
print(node.hex2str(foo))

from js2pysecrets.settings import Settings
import js2pysecrets as secrets

# Initilize Settings
settings = Settings()
defaults = settings.get_defaults()

# Accessing bits Variables
print(defaults.size) # 8

# Update bits Variables
settings.update_defaults(size=16)
print(defaults.size) # 16   

settings = Settings()
print(settings.size)


