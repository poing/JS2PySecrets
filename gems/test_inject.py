#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# test_inject.py

#from test_func import forTesting

TESTER = False

# Set the global variable TESTER to True to inject behavior
def run_test():
	global TESTER  # Use the global keyword to modify the global variable
	TESTER = True

	# Call the forTesting function as usual
	result = forTesting()
	return result
	
#print(run_test())  # Expected result "Hello Developer"
print(TESTER)
#print(run_test())
print(False)