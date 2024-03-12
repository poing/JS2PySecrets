#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test.py

import subprocess

# Start the subprocess
node_daemon = subprocess.Popen(
    ["node"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)


# def read(process):
#     return node_daemon.stdout.readline()
# 
# 
# def write(process, message):
#     node_daemon.stdin.write(message)
#     node_daemon.stdin.flush()
# 
# 
# def terminate(process):
#     node_daemon.stdin.close()
#     node_daemon.terminate()
#     node_daemon.wait(timeout=0.2)
# 
# input_data = "console.log(`hello`);"
# 
# write(node_daemon, input_data)
# print(read(node_daemon))
# terminate(node_daemon)

# Send input data to the subprocess
input_data = "console.log(`what`);"
node_daemon.stdin.write(input_data + "\n")
a = node_daemon.stdout

#node_daemon.communicate(input=input_data)
#node_daemon.stdin.flush()
#node_daemon.stdout.flush()
#node_daemon.stdin.flush()
#print(node_daemon.stdout)
#print(node_daemon.stdout.readline())
#x = open(node_daemon.stdout, "r")
#print(str(x))
#node_daemon.stdin.flush()
#print(node_daemon.stdout.readline())

# Send input data to the subprocess
#input_data = "console.log(`what`);"
#output, _ = node_daemon.communicate(input=input_data)

# Print the output
#print("Output from subprocess:", output)

# Send input data to the subprocess
#input_data = "console.log(`why`);"
#output, _ = node_daemon.communicate(input=input_data)

# Print the output
#print("Output from subprocess:", output)


input_data = "console.log(`where`);"
node_daemon.stdin.write(input_data + "\n")
#node_daemon.communicate(input=input_data)
#print(node_daemon.stdout.readline())
b = node_daemon.stdout


input_data = "console.log(`when`);"
node_daemon.stdin.write(input_data + "\n")
#node_daemon.communicate(input=input_data)
#print(node_daemon.stdout.readline())

# Close the stdin to indicate that we're done sending input
#node_daemon.stdin.flush()

node_daemon.stdin.close()
#node_daemon.communicate()

print(b.readline())

# Read the output and errors
output_lines = []
while True:
    output_line = node_daemon.stdout.readline()
    if not output_line:
        break
    output_lines.append(output_line)

errors_lines = []
while True:
    error_line = node_daemon.stderr.readline()
    if not error_line:
        break
    errors_lines.append(error_line)

# Print the output and errors
print("Output from subprocess:")
print("".join(output_lines))

print("Errors from subprocess:")
print("".join(errors_lines))

