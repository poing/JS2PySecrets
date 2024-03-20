#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# defaults.py

import json
import js2pysecrets as secrets
from js2pysecrets.settings import Settings
import random

# This does not work
settings = Settings()
defaults = settings.get_defaults()

# @dataclass
# class Defaults:
#     theRNG = lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits)
#     bits: int = 8  # default number of bits
#     radix: int = 16  # work with HEX by default

bits = 64
random_binary = defaults.rng(bits)
print("Random binary:", random_binary)

print("---")

# This works
settings = Settings()
defaults = settings.get_defaults()
bits = 64
defaults.rng = lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits)
random_binary = defaults.rng(bits)
print("Random binary:", random_binary)

# print(random_binary)
# 
# hex_data = secrets.bin2hex(random_binary)
# 
# print(hex_data) 
# 
# print(secrets.hex2bin(hex_data).zfill(config.bits))


def getRandom(bits):
	if isinstance(config.rng, str):
	# if isinstance(config.rng, str) and (config.rng == "testRandom"):
		# Call the real function
		random_binary_string = test_random(bits)
		return "Random binary using string representation:", random_binary_string
	else:
		# Call the lambda expression
		random_binary_string = config.rng(bits)
		return "Random binary using lambda expression:", hex(int(random_binary_string, 2))[2:]


settings = Settings()
settings.update_defaults(bits=8)
config = settings.get_config()
print('ZZZZZZZZZZZZZZZZZZ', config.rng(8))

random_binary = config.rng(16)

print(random_binary)
print(config.bits % len(random_binary), "/", len(random_binary))


hex_data = secrets.bin2hex(random_binary)

print(hex_data) 

hex_value = secrets.hex2bin(hex_data)

print(hex_value)
print((len(hex_value)%config.bits)%config.bits, "/", len(hex_value))


config.rng = "testRandom"
print(getRandom(22))



# # Accessing Defaults
# settings = Settings()
# defaults = settings.get_defaults()
# print(defaults.bits)  # Output: 8
# 
# # Updating Defaults
# settings.update_defaults(bits=16)
# defaults = settings.get_defaults()
# print(defaults.bits)  # Output: 16
# 
# # Reverting to Default Values
# settings.update_defaults()
# defaults = settings.get_defaults()
# print(defaults.bits)  # Output: 8 (reverted to the default value)
# 
# # Updating Defaults
# settings.update_defaults(bits=16)
# defaults = settings.get_defaults()
# print(defaults.bits)  # Output: 16
# 
# # Reverting to Default Values
# settings.reset_defaults()
# defaults = settings.get_defaults()
# print(defaults.bits)  # Output: 8 (reverted to the default value)
# 
# print(defaults.theRNG(33))
# 
# print(defaults.primitive_polynomials[12])
# 
# settings.update_defaults(bits=99)
# print(defaults)
# 
# settings = Settings()
# settings.reset_defaults()
# 
# config = settings.get_config()
# # I want this
# print(config.bits)
# print(config.radix)
# print(config)

# Do not want this
#print(config['bits'])
#print(config['radix'])
#print(config)

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
config = settings.get_config()
secrets.setRNG()
print(config.rng(8))


secrets.setRNG('hello')
config = settings.get_config()
print(config.rng)
secrets.setRNG(lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits))
config = settings.get_config()

print(config.rng(8))
#config.rng(8)


