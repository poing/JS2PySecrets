#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV2_test.py

"""
This script demonstrates the second working version of calling Node.js to execute JavaScript using a wrapper to load the secrets.js package.
This version handles multiple commands, sent as setup and start.
"""

import json
import subprocess

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV2.js"

def run_js_functions(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data (dict): Dictionary containing the function name and arguments.

    Returns:
        The result of the JavaScript function or None if there is an error.
    """
    #input_json = json.dumps(input_data) #Removed this
    
    # Enclose input_json in single quotes
    js_command = ["node", JS_FILE_PATH, input_data]
    
    try:
        # Run the command and capture the output
        result = subprocess.run(js_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Debugging statement to print stdout and stderr
        #print("stdout:", result.stdout)
        #print("stderr:", result.stderr)

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
# Setup commands
setup = [
    {'function': 'setRNG', 'args': ['testRandom']},
]

# Dynamic Values
foo = ['1234abc', 6, 3]

# Main function
main = {'function': 'share', 'args': foo}

# Combine setup and main
tasks = {'tasks': [{'setup': setup, 'start': main}]}

# Convert the Python dictionary to JSON
json_data = json.dumps(tasks, indent=None)
#print(json_data)

js_result = run_js_functions(json_data)

# You can uncomment the following examples if needed
# ...



# # Example usage
# # Example 1: Convert hexadecimal to binary
# function_name = "_hex2bin"
# arguments = ["ABAB"]
# js_result = run_js_function(function_name, arguments)
# 
# # Compare with the Python result
# expected_python_result = bin(int("ABAB", 16))[2:]
# print("Expected Python Result:", expected_python_result)
# 
# if js_result is not None:
#     assert js_result == expected_python_result
# else:
#     print("Test failed: JavaScript result is None or missing 'result' key.")
# 
# # Example 2: Left pad a binary string
# function_name = "_padLeft"
# arguments = ["111", 32]
# js_result = run_js_function(function_name, arguments)
# 
# # Example 3: Call the 'share' function
# function_name = "share"
# arguments = ["1234abc", 6, 3]
# js_result = run_js_function(function_name, arguments)
# 
# # Example 4: Generate a random string
# function_name = "random"
# arguments = [32]
# js_result = run_js_function(function_name, arguments)




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