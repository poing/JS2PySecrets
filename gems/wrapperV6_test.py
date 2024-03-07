#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV6_test.py

"""
This script demonstrates the third working version of calling Node.js to execute JavaScript using a wrapper to load the secrets.js package.
This version handles multiple commands, sent as setup and start.  And have improved error handling.
"""

import json
import subprocess
import ast

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV6.js"

def wrapper(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data (dict): Dictionary containing the function name and arguments.

    Returns:
        The result of the JavaScript function or None if there is an error.
    """
    
    # Enclose input_json in single quotes
    js_command = ["node", JS_FILE_PATH, input_data]
    print("Input data sent to JavaScript:", input_data)
    
    try:
        # Run the command and capture the output and stderr
        result = subprocess.run(js_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        
        # Debugging statement to print stdout and stderr
        print("Result stdout:", result.stdout)
        print("Result stderr:", result.stderr)

        try:
            # Attempt to load the entire stdout as JSON
            js_result = json.loads(result.stdout)
            print('json.loads')
            
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
            print("Python error decoding JSON:", e)
            print("Raw stdout content:", result.stdout)

    except subprocess.CalledProcessError as e:
        # Print the error from the JavaScript script
        js_error = result.stderr.strip()
        print("JavaScript error:", js_error)
        return None

class JsFunction:
    def __init__(self, func, test=False):
        self.func = func
        self.test = test

    def __call__(self, *args, test=False, **kwargs):
        def wrapped_func(*args, **kwargs):
            args_str = ', '.join(repr(arg) for arg in args)
            #kwargs_str = ', '.join(f'{key}={repr(value)}' 
            #	for key, value in kwargs.items())
            #all_args = ', '.join(filter(None, [args_str, kwargs_str]))

            return f"{self.func.__name__}({args_str})"
            
        data = []
        
        # DO NOT REMOVE THIS
        if test or self.test:
        	data.append("setRNG('testRandom')")

        data.append(wrapped_func(*args, **kwargs) if args else self.func(*args, **kwargs))
        return data

    def __get__(self, instance, owner):
        return self if instance is None else types.MethodType(self, instance)

@JsFunction
def init(*args, **kwargs):
    pass 
    
@JsFunction
def setRNG(*args, **kwargs):
    pass 

@JsFunction
def share(*args, **kwargs):
    pass 



alpha = init(33)
bravo = setRNG("testRandom")
delta = share('1234abc', 6, 3)


# Combine
tasks = [
	alpha,
	bravo,
	delta,
	share(["aaa"],["bbb"], ["ccc"])
]

print("Tasks: ", tasks)

#tasks = delta

json_data = json.dumps(tasks, indent=None)
#print("JSON Data: ", json_data) # [["init(33)"], ["setRNG('testRandom')"], ["share('1234abc', 6, 3)"]]


js_result = wrapper(json_data)
print(js_result)

# # Working Example: Valid JavaScript: share('1234abc', 6, 3); 
# # Setup commands
# setup = [
#     {'function': 'setRNG', 'args': ['testRandom']},
# ]
# 
# # Dynamic Values
# foo = ['1234abc', 6, 3]
# 
# # Main function
# main = {'function': 'share', 'args': foo}
# 
# # Combine setup and main
# tasks = {'tasks': [{'setup': setup, 'start': main}]}
# 
# # Convert the Python dictionary to JSON
# json_data = json.dumps(tasks, indent=None)
# #print(json_data)
# 
# js_result = run_js_functions(json_data)
# print(js_result)
# 
# 
# # Problem Example: Invalid JavaScript: combine(['8027e7e7e7e7e7e7e7e7e7e7e7e6f5d34c2', '805191919191919191919191919083a53a5', '80667676767676767676767676776442ddb']); 
# # Setup commands
# setup = [
#     {'function': 'setRNG', 'args': ['testRandom']},
# ]
# 
# # Dynamic Values
# foo = ['8027e7e7e7e7e7e7e7e7e7e7e7e6f5d34c2', '805191919191919191919191919083a53a5', '80667676767676767676767676776442ddb']
# 
# # Main function
# main = {'function': 'combine', 'args': foo}
# 
# # Combine setup and main
# tasks = {'tasks': [{'setup': setup, 'start': main}]}
# 
# # Convert the Python dictionary to JSON
# json_data = json.dumps(tasks, indent=None)
# #print(json_data)
# 
# js_result = run_js_functions(json_data)
# print(js_result)

