#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# defaults.py

import js2pysecrets.base

def test_functions_exist():
    # List of functions you expect to exist in your_module
    expected_functions = [
        'init',
        'combine',
        'getConfig',
        'extractShareComponents',
        'setRNG',
        'str2hex',
        'hex2str',
        'random',
        'share',
        'newShare',
        '_reset',
        '_padLeft',
        '_hex2bin',
        '_bin2hex',
        '_hasCryptoGetRandomValues',
        '_hasCryptoRandomBytes',
        '_getRNG',
        '_isSetRNG',
        '_splitNumStringToIntArray',
        '_horner',
        '_lagrange',
        '_getShares',
        '_constructPublicShareString'
    ]

    # List to collect missing functions
    missing_functions = []

    # Loop through each function name and check if it exists in your_module
    for func_name in expected_functions:
        if not hasattr(your_module, func_name):
            missing_functions.append(func_name)

    # Print the list of missing functions
    if missing_functions:
        print("Functions to create:")
        for missing_func in missing_functions:
            print(missing_func)
    else:
        print("All expected functions exist.")
