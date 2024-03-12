#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV11_test.py


def getFixedBitString(bits):
    return str(123456789)[:bits]
    
print(getFixedBitString(22))

print(getFixedBitString(5))