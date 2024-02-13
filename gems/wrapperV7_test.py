#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV7_test.py

import subprocess

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV7.js"

def wrapper(input_data):
    js_command = ["node", JS_FILE_PATH, input_data]
    print("Input data sent to JavaScript:", input_data)

    try:
        # Run the command and capture the output and stderr
        result = subprocess.run(js_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("Output from JavaScript:", result.stdout)
        print("Errors from JavaScript:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error running JavaScript script:", e)

# Strings to be passed as input_data
one = "init(33)"
two = "setRNG('something')"
three = 'share("AABB", 6, 3)'

# Concatenate the strings
input_data = ";".join([one, two, three])

# Call the wrapper function with input_data without quotes
wrapper(input_data)
