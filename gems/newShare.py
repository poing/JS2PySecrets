#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# splitNumStringToIntArray.py.py

import random
import js2pysecrets as secrets
from js2pysecrets.settings import Settings
settings = Settings()


secrets.init(8)
secret = secrets.random(32)
print('Secret: ', secret)

shares = secrets.share(secret, 6, 3)
print(shares)

result = secrets.newShare(7, shares)
print(result)

# Select a number of random shares
def pieces(shares, number=3):
    random.shuffle(shares)  # Randomize
    return shares[-number:]
    
chunks = pieces(shares, 2)
chunks.append(result)
print(chunks)    

print(secrets.combine(chunks))