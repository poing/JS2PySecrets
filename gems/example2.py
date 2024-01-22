#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# example1.py

import json
import js2pysecrets

# var pw = "<<PassWord123>>"
pw = "<<PassWord123>>"
 
# // convert the text into a hex string
# var pwHex = secrets.str2hex(pw) // => hex string
jsHex = js2pysecrets.str2hex(pw)
print(jsHex)

pyHex = pw.encode('utf-16-be').hex().lstrip('fe')
print(pyHex)

# // split into 5 shares, with a threshold of 3
# var shares = secrets.share(pwHex, 5, 3)
# 
# // combine 2 shares:
# var comb = secrets.combine(shares.slice(1, 3))
# 
# //convert back to UTF string:
# comb = secrets.hex2str(comb)
# console.log(comb === pw) // => false
# 
# // combine 3 shares:
# comb = secrets.combine([shares[1], shares[3], shares[4]])
# 
# //convert back to UTF string:
# comb = secrets.hex2str(comb)
# console.log(comb === pw) // => true