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
	random_list.append(int(random_string, 2))	
	
#print(settings.dithering)

#test = lambda bits: bin(1+random.getrandbits(bits))[2:].zfill(bits)

#print(test(2345))

secrets.init(8)
#secrets.init()
#print(max(settings.logs[1:]))

settings.update_defaults(dithering=lambda string: dithering(string))

results = secrets.share('00740073006500740020000020007300690073006900680074', 50, 3)
results = secrets.share('00740073006500740020610020007300690073006900680074', 60, 3)
results = secrets.share('00740073006500742000610020007300690073006900680074', 70, 3)
results = secrets.share('00740073006504002000610020007300690073006900680074', 50, 3)
results = secrets.share('00740073000074002000610020007300690073006900680074', 50, 3)
results = secrets.share('00740070650074002000610020007300690073006900680074', 50, 3)
results = secrets.share('00747300650074002000610020007300690073006900680074', 50, 3)

print(results)

print(random_list, len(random_list))