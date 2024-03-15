#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# wrapperV11_test.py


import random

def test_random(bits):
    radix = 10
    size = 32
    elems = -(-bits // 32)  # Equivalent to ceil(bits / 32)
    integer = 123456789
    arr = [str(integer)] * elems

    str_result = None

    while str_result is None:
        str_result = construct(bits, arr, radix, size)

    return str_result

def construct(bits, arr, radix, size):
    i = 0
    str_result = ""
    parsed_int = 0

    if arr:
        len_arr = len(arr) - 1

    while i < len_arr or len(str_result) < bits:
        # convert any negative numbers to positive with abs()
        parsed_int = abs(int(arr[i], radix))
        str_result += pad_left(bin(parsed_int)[2:], size)
        i += 1

    str_result = str_result[-bits:]

    # return None so this result can be re-processed if the result is all 0's.
    if str_result.count('0') == len(str_result):
        return None

    return str_result

def pad_left(s, size):
    return '0' * (size - len(s)) + s

# Example usage:
result = test_random(64)
print(result)




import secrets

def generate_random_binary(bits):
    return bin(secrets.randbits(bits))[2:].zfill(bits)

# Example usage:
random_binary = generate_random_binary(256)
print(random_binary)


def bin_to_hex(binary_string):
    # Convert binary string to integer
    integer_value = int(binary_string, 2)
    # Convert integer to hexadecimal string
    hex_string = hex(integer_value)[2:]
    return hex_string

# Example usage:
binary_string = '10101010'
hexadecimal_string = bin_to_hex(test_random(64))
print(hexadecimal_string)

bits = 64

# This would be a real function
def test_random(bits):
  # returns binary value

config.rng = lambda: bin(secrets.randbits(bits))[2:].zfill(bits)
print(config.rng(bits)

config.rng = "test_random"
print(config.rng(bits)






