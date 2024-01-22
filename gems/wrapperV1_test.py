#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV1_test.py

"""
This script demonstrates the first working version of calling Node.js to execute JavaScript using a wrapper to load the secrets.js package.
It's rudimentary and currently only handles one (1) command. But it works!

The example usage at the end showcases calling different JavaScript functions with corresponding arguments and the rudimentary goal of comparing the results with Python calculations.
"""

import json
import subprocess

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV1.js"

def run_js_function(function_name, arguments):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        function_name (str): Name of the JavaScript function to call.
        arguments (list): List of arguments to pass to the JavaScript function.

    Returns:
        The result of the JavaScript function or None if there is an error.
    """
    input_data = {
        "functionName": function_name,
        "arguments": arguments
    }
    input_json = json.dumps(input_data)
    
    js_command = ["node", JS_FILE_PATH, input_json]
    
    try:
        # Run the command and capture the output
        result = subprocess.run(js_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Debugging statement to print stdout and stderr
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        try:
            # Attempt to load the entire stdout as JSON
            js_result = json.loads(result.stdout)
            
            # Check if the result is "None" or missing 'result' key
            if js_result is not None and "result" in js_result:
                extracted_result = js_result.get("result", None)
                print("Extracted JavaScript result:", extracted_result)
                return extracted_result
            else:
                print("JavaScript result is None or missing 'result' key.")
                return None
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Raw stdout content:", result.stdout)
            return None

    except subprocess.CalledProcessError as e:
        print("Error executing subprocess:", e)
        return None

# Example usage
# Example 1: Convert hexadecimal to binary
function_name = "_hex2bin"
arguments = ["ABAB"]
js_result = run_js_function(function_name, arguments)

# Compare with the Python result
expected_python_result = bin(int("ABAB", 16))[2:]
print("Expected Python Result:", expected_python_result)

if js_result is not None:
    assert js_result == expected_python_result
else:
    print("Test failed: JavaScript result is None or missing 'result' key.")

# Example 2: Left pad a binary string
function_name = "_padLeft"
arguments = ["111", 32]
js_result = run_js_function(function_name, arguments)

# Example 3: Call the 'share' function
function_name = "share"
arguments = ["1234abc", 6, 3]
js_result = run_js_function(function_name, arguments)

# Example 4: Generate a random string
function_name = "random"
arguments = [32]
js_result = run_js_function(function_name, arguments)




# # # Example usage
# function_name = "_hex2bin"
# arguments = ["ABAB"]
# js_result = run_js_function(function_name, arguments)
# # 
# # # Compare with the Python result
# # expected_python_result = bin(int("ABAB", 16))[2:]
# # print("Expected Python Result:", expected_python_result)
# # 
# # if js_result is not None:
# #     assert js_result == expected_python_result
# # else:
# #     print("Test failed: JavaScript result is None or missing 'result' key.")
# # 
# function_name = "_padLeft"
# arguments = ["111", 32]
# js_result = run_js_function(function_name, arguments)
# # 
# # 
# function_name = "share"
# arguments = ["1234abc", 6, 3]
# js_result = run_js_function(function_name, arguments)
# # 
# # # function_name = "getConfig"
# # # arguments = []
# # # js_result = run_js_function(function_name, arguments)
# # # 
# # function_name = "random"
# # arguments = [32]
# # js_result = run_js_function(function_name, arguments)