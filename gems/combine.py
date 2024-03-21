#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# defaults.py

import js2pysecrets.node as node

import js2pysecrets as secrets
from js2pysecrets.settings import Settings
settings = Settings()

secrets.init()
secret = secrets.random(32)
shares = secrets.share(secret, 6, 3)

print("Secret: ", secret)
print(secrets.combine(shares))





