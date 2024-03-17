#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test.py

import json
#from js2pysecrets import share, combine
import js2pysecrets.node as node


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

# data = js2pysecrets.random(64)
# print(js2pysecrets.str2hex(data))
#random = js2pysecrets.jsFunction('random', test=True)
#print(random(32))
# print(node.random(32))
# print(share("ababab", 6, 3, test=True))
# 
# shares = node.share("ababab", 6, 3)
# print(shares[1])
# print(shares[3])
# print(shares[5])
# 
# recoveredPass = combine([shares[1],shares[3],shares[5]])
# print("recovered password is: ", recoveredPass)
# 
# node.random(0)

print(node.nodeCryptoRandomBytes(32))
print(node.nodeCryptoRandomBytes(32))
print(node.nodeCryptoRandomBytes(32))
print(node.nodeCryptoRandomBytes(32))
print(node.nodeCryptoRandomBytes(32))
print(node.nodeCryptoRandomBytes(32))

print(node.testRandom(32))
print(node.testRandom(32))
print(node.testRandom(32))
print(node.testRandom(16))
print(node.testRandom(32))