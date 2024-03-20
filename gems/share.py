#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# splitNumStringToIntArray.py.py

import random
import js2pysecrets as secrets
from js2pysecrets.settings import Settings
settings = Settings()



random_list=[]
def dithering(random_string):
	#random_list.append('hello')
	random_list.append(hex(int(random_string)))	
	
#print(settings.dithering)

#test = lambda bits: bin(1+random.getrandbits(bits))[2:].zfill(bits)

#print(test(2345))

secrets.init(4)
#secrets.init()
#print(max(settings.logs[1:]))

#settings.update_defaults(dithering=lambda string: dithering(string))

results = secrets.share('0074007300650074002000610020007300690073006900680074', 6, 3)

print(results)

#print(random_list)