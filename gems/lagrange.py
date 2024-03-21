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

print(secrets.lagrange(0, [2,3,5], [113,211,22]))


print(secrets.lagrange(0, [2,3,5], (113,211,22)))



