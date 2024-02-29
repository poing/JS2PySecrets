#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapper.py

"""
This script is a revised version for calling Node.js to execute JavaScript using a wrapper to load the secrets.js package.
This version handles multiple commands with a list, encodes the list to base36 for the CLI, and has improved error handling.
"""

import json
import os
import subprocess

# Path to the Node.js wrapper script
#JS_FILE_PATH = "./javascript/wrapper.js"

def wrapper(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data [list]: List of functions with arguments.

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
        
        # Debugging statements to print stdout and stderr
        # print("Input data sent to JavaScript:", input_data)
        # print("stdout:", result.stdout)
        # print("stderr:", result.stderr)

        try:
            # Attempt to load the entire stdout as JSON
            js_result = json.loads(result.stdout)
            #print('json.loads')
            
            # Print stderr if it exists
            if result.stderr:
                print("JavaScript stderr:", result.stderr)
                
            return js_result

        except json.JSONDecodeError as e:
            print("Python error decoding JSON:", e)
            print("Raw stdout content:", result.stdout)

    except subprocess.CalledProcessError as e:
        # Print the error from the JavaScript script
        js_error = e.stderr.strip()  # Use e.stderr instead of result.stderr
        print("JavaScript error:", js_error)
        return None