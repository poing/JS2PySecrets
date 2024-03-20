#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# splitNumStringToIntArray.py.py

import js2pysecrets as secrets
import random

data = ['remove me', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj']
print(data)
data.pop(0)
random.shuffle(data)
print(data)
print(data[-3:])


def pieces(shares, number=3):
	shares.pop(0) # Remove first share
	random.shuffle(shares) # Randomize
	return shares[-number:]
	
data = ['remove me', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj']

for i in range(10):
	data = ['remove me', 'bb', 'cc', 'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj']
	print(pieces(data))