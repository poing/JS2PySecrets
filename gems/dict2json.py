#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

import json

# Example data
setup = {
	"setup" :
	[
  		{"function": "setRNG", "args": "testRandom"},
  		{"function": "init", "args": "12, 'testRandom'"}
	]
}

foo = "'1234abc', 6, 3"

command = {
	"start" : {"function": "share", "args": foo}
}
new_site = setup | command

# Convert the Python dictionary to JSON
json_data = json.dumps(new_site, indent=2)

# Print or use the JSON data as needed
print(json_data)
