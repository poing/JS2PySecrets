#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV9_test.py

import json
import subprocess

# Path to the Node.js wrapper script
JS_FILE_PATH = "wrapperV9.js"

def wrapper(input_data):
    """
    Run a JavaScript function using the Node.js wrapper.

    Args:
        input_data (list): List containing the function calls as strings.

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
        
        #print("Input data sent to JavaScript:", input_data)
        
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
        js_error = e.stderr.strip()  # Use e.stderr instead of result.stderr
        print("JavaScript error:", js_error)
        return None

'''
Used to pass a "clean" string as an arg to the CLI
'''
def encode_to_base36(data):
    base36_string = ""
    for key, value in data.items():
        base36_string += key + str(value)
    return base36_string

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



json_data = json.dumps(tasks, indent=None).replace("'", "`")
#print(json_data)
#print(json_data.encode().hex())
data = json_data.encode().hex()
#print(data) 
# Call the wrapper function
js_result = wrapper(data)
#print(js_result)
