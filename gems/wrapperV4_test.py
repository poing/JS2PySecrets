#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV4_test.py

"""
This script demonstrates the another working version, based on V3, calling Node.js to execute JavaScript using a wrapper to load the secrets.js package.
This version handles multiple commands, sent as setup and start.  And have improved error handling.  But there is an issue passing array data to the JS.  combine(["aa", "bb", "cc"]); does not work in the wrapper.
"""

import json
import subprocess

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV4.js"

# ... (previous code)

def run_js_functions(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data (dict): Dictionary containing the function name and arguments.

    Returns:
        The result of the JavaScript function or None if there is an error.
    """
    
    # Enclose input_json in single quotes
    js_command = ["node", JS_FILE_PATH, input_data]
    
    try:
        # Run the command and capture the output and stderr
        result = subprocess.run(js_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Debugging statement to print stdout and stderr
        # print("stdout:", result.stdout)
        # print("stderr:", result.stderr)

        try:
            # Attempt to load the entire stdout as JSON
            js_result = json.loads(result.stdout)
            
            # Check if the result has 'error' or 'results' key
            if js_result is not None and "results" in js_result:
                start_result = js_result.get("results", [])[0].get("startResult", {}).get("result")
                if start_result is not None:
                    print("Result of 'start' function:", start_result)
                else:
                    print("No result found for 'start' function.")
            elif js_result is not None and "error" in js_result:
                print("JavaScript error:", js_result.get("error"))
            else:
                print("JavaScript output is missing 'error' or 'results' key.")
                
            # Print stderr if it exists
            if result.stderr:
                print("JavaScript stderr:", result.stderr)
                
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Raw stdout content:", result.stdout)

    except subprocess.CalledProcessError as e:
        # Print the error from the JavaScript script
        js_error = result.stderr.strip()
        print("JavaScript error:", js_error)
        return None


# Working Example: Valid JavaScript: share('1234abc', 6, 3); 
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

print(tasks)


# Convert the Python dictionary to JSON
json_data = json.dumps(tasks, indent=None)

# Run the JavaScript functions
js_result = run_js_functions(json_data)
print(js_result)

# Problem Example: Invalid JavaScript: combine(['8027e7e7e7e7e7e7e7e7e7e7e7e6f5d34c2', '805191919191919191919191919083a53a5', '80667676767676767676767676776442ddb']); 
# Setup commands
setup = [
    {'function': 'setRNG', 'args': ['testRandom']},
]

# Dynamic Values
foo = [
    '8027e7e7e7e7e7e7e7e7e7e7e7e6f5d34c2',
    '805191919191919191919191919083a53a5',
    '80667676767676767676767676776442ddb'
]

# Main function
main = {'function': 'combine', 'args': [foo]}

# Combine setup and main
tasks = {'tasks': [{'setup': setup, 'start': main}]}

print(tasks)

# Convert the Python dictionary to JSON
json_data = json.dumps(tasks, indent=None)

# Run the JavaScript functions
js_result = run_js_functions(json_data)
print(js_result)

