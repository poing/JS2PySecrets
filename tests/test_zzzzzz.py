#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# defaults.py

# test_functions_exist.py

import js2pysecrets.base as secrets  # Import the module you want to test


def test_functions_exist():
    # List of functions you expect to exist in secrets
    expected_functions = [
        "init",
        "combine",
        "getConfig",
        "extractShareComponents",
        "setRNG",
        "str2hex",
        "hex2str",
        "random",
        "share",
        "newShare",
        "reset",
        "padLeft",
        "hex2bin",
        "bin2hex",
        "hasCryptoGetRandomValues",
        "hasCryptoRandomBytes",
        "getRNG",
        "isSetRNG",
        "splitNumStringToIntArray",
        "horner",
        "lagrange",
        "getShares",
        "constructPublicShareString",
    ]

    # List to collect missing functions
    missing_functions = []

    # Loop through each function name and check if it exists in secrets
    for func_name in expected_functions:
        if not hasattr(secrets, func_name):
            missing_functions.append(func_name)

    # Print the list of missing functions
    if missing_functions:
        print("Functions to create:")
        for missing_func in missing_functions:
            print(missing_func)
        print(
            "Percentage: ",
            format(
                1 - (len(missing_functions) / len(expected_functions)), ".2%"
            ),
        )
    else:
        print("All expected functions exist.")
