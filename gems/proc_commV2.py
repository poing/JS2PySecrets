#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# proc_commV2.py

# Trying to use process.communicate() with Node

import subprocess

#JS_FILE_PATH = "wrapperV7.js"
#js_command = ["node", "-i", JS_FILE_PATH]

# Start the Node.js process
node_process = subprocess.Popen(["node", "-i"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Send JavaScript commands
commands = [
	"const secrets = require('../secrets.js/secrets.js')",
    "console.log('Hello from Node.js!')",
    "console.log(2 + 2)",
    "console.log(Math.random())",
    "var HHGTTG = 42",
    "console.log(HHGTTG)",
    "secrets.share('1234abc', 6, 3)"
]

#print(commands[0])

# Send commands to the Node.js process
for command in commands:
    node_process.stdin.write(command + '\n')
#node_process.stdin.write(commands[1] + '\n')
#foo.stdout.readline()

# Read output
output, error = node_process.communicate()

# Close stdin to indicate end of input
node_process.stdin.close()


print("Output:")
print(output)

print("Error:")
print(error)