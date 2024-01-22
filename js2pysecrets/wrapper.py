#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapper.py

"""
This script demonstrates the third working version of calling Node.js to execute JavaScript using a wrapper to load the secrets.js package.
This version handles multiple commands, sent as setup and start.  And have improved error handling.
"""

import json
import subprocess
import os

# Path to the Node.js wrapper script
JS_FILE_PATH = "./javascript/wrapper.js"

def wrapper(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data (dict): Dictionary containing the function name and arguments.

    Returns:
        The result of the JavaScript function or None if there is an error.
    """
    
    # Get the directory where this Python script is located
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Change the current working directory to the directory containing the wrapper.js file
    os.chdir(os.path.join(script_directory, '..', 'javascript'))
    
    # Call the wrapper
    js_command = ["node", "wrapper.js", input_data]
    
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
                    return(start_result)
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



