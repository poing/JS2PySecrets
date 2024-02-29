#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV7_test.py

import json
import subprocess

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV7.js"

def wrapper(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data (list): List containing the function calls as strings.

    Returns:
        The result of the JavaScript function or None if there is an error.
    """
    
    # Convert the list to JSON string
    json_data = json.dumps(input_data)
    print("Input data sent to JavaScript:", json_data)
    
    try:
        # Run the command and capture the output and stderr
        result = subprocess.run(["node", JS_FILE_PATH, json_data], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Debugging statement to print stdout and stderr
        print("Result stdout:", result.stdout)
        print("Result stderr:", result.stderr)

        try:
            # Attempt to load the entire stdout as JSON
            js_result = json.loads(result.stdout)
            print('json.loads')
            
            # Print stderr if it exists
            if result.stderr:
                print("JavaScript stderr:", result.stderr)
                
            return js_result

        except json.JSONDecodeError as e:
            print("Python error decoding JSON:", e)
            print("Raw stdout content:", result.stdout)

    except subprocess.CalledProcessError as e:
        # Print the error from the JavaScript script
        js_error = result.stderr.strip()
        print("JavaScript error:", js_error)
        return None

# Define tasks
tasks = [
    "init(33)",
    "setRNG('testRandom')",
    "share('1234abc', 6, 3)",
    "share(['aaa'], ['bbb'], ['ccc'])"
]

# Call the wrapper function
js_result = wrapper(tasks)
print(js_result)
