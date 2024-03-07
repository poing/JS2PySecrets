#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# example1.py

import json
import js2pysecrets

# // generate a 512-bit key
# key = js2pysecrets.random(512) // => key is a hex string
key = js2pysecrets.random(512)
print(key)

# // split into 10 shares with a threshold of 5
# shares = js2pysecrets.share(key, 10, 5)
# // => shares = ['801xxx...xxx','802xxx...xxx','803xxx...xxx','804xxx...xxx','805xxx...xxx']
shares = js2pysecrets.share(key, 10, 5)
print(shares)

# // combine 4 shares
# var comb = secrets.combine(shares.slice(0, 4))
# console.log(comb === key) // => false
#
# // combine 5 shares
# comb = secrets.combine(shares.slice(4, 9))
# console.log(comb === key) // => true
# 
# // combine ALL shares
# comb = secrets.combine(shares)
# console.log(comb === key) // => true
# 
# // create another share with id 8
# var newShare = secrets.newShare(8, shares) // => newShare = '808xxx...xxx'
# 
# // reconstruct using 4 original shares and the new share:
# comb = secrets.combine(shares.slice(1, 5).concat(newShare))
# console.log(comb === key) // => true