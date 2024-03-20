#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test.py

import subprocess
import threading
import queue
import select

def read_output(process, output_queue):
    while process.poll() is None:  # Check if the process is still running
        ready, _, _ = select.select([process.stdout], [], [], 0.1)  # Wait for 0.1 second for data to be available
        if process.stdout in ready:
            output_line = process.stdout.readline().strip()
            if output_line:
                output_queue.put(output_line)

# Start the subprocess
node_daemon = subprocess.Popen(
    ["node"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

# Create a queue for output data
output_queue = queue.Queue()

# Create and start a thread for reading output
output_thread = threading.Thread(target=read_output, args=(node_daemon, output_queue))
output_thread.start()

# Send input data to the subprocess
node_daemon.stdin.write("console.log('Hello from subprocess');\n")
node_daemon.stdin.flush()

# Read output from the queue
while True:
    try:
        output_line = output_queue.get(timeout=1)  # Wait for 1 second for output to be available
        print("Output from subprocess:", output_line)
    except queue.Empty:
        if node_daemon.poll() is not None:  # Check if the process has terminated
            break

# Wait for the output thread to finish
output_thread.join()

# Close the subprocess
node_daemon.stdin.close()
node_daemon.wait()
