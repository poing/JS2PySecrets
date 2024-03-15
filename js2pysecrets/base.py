# import json

# from .decorators import JsFunction, jsNeedless

# from .wrapper import wrapper  # Import your wrapper function

import math

from js2pysecrets.settings import Settings

NAME = "js2pysecrets"


settings = Settings()
# settings.update_defaults(rng=99)
# config = settings.get_config()


def isSetRNG():
    config = settings.get_config()
    if isinstance(config.rng, str) or callable(config.rng):
        return True
    return False


def bin2hex(binary_string: str) -> str:
    return hex(int(binary_string, 2))


def hex2bin(hex_string: str) -> str:
    return bin(int(hex_string, 16))


"""
Adapted Python Random Number Generation:

This module provides a Python adaptation of the JavaScript code for random
number generation. It offers a minimalistic approach to replicating the
functionality present in the JavaScript version.

The `setRNG` function mirrors the logic of the JavaScript function. If it's a
string, ANY STRING, it implies a specific type is requested. In such cases,
it will function like the JavaScript `test_random` RNG for testing purposes.

This adaptation aims to maintain the core functionality of the JavaScript
version while adhering to Python idioms and conventions. The focus is on
providing a concise implementation that retains the essential features
of the original JavaScript code.

This code also allows a lambda expression representing a custom RNG for random
number generation.

Example usage:
    import random

    # Use a custom RNG
    setRNG(lambda bits: bin(random.getrandbits(bits)))

Deprecated variables:
- `config.typeCSPRNG`: This variable is deprecated and maintained for
backward compatibility. This variable has no affect in the current code.
"""


# lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits)
def setRNG(new_rng=None):
    config = settings.get_config()
    new_rng = new_rng or config.rng
    settings.update_defaults(rng=new_rng)
    return True


def str2hex(string, bytes_per_char=None):
    if not isinstance(string, str):
        raise ValueError("Input must be a character string.")

    defaults = settings.get_defaults()

    # defaults = {"bytes_per_char": 2, "max_bytes_per_char": 4}
    # Assuming these defaults
    if bytes_per_char is None:
        bytes_per_char = defaults.bytes_per_char

    if (
        not isinstance(bytes_per_char, int)
        or bytes_per_char < 1
        or bytes_per_char > defaults.max_bytes_per_char
    ):
        raise ValueError(
            f"Bytes per character must be an integer between 1 and "
            f"{defaults.max_bytes_per_char}, inclusive."
        )

    hex_chars = 2 * bytes_per_char
    max_val = 16**hex_chars - 1

    out = ""
    for char in string:
        num = ord(char)

        if num > max_val:
            needed_bytes = math.ceil(
                math.log(num + 1) / math.log(256)
            )  # pragma: no cover  Too difficult to test
            raise ValueError(
                f"Invalid character code ({num}). Maximum allowable is "
                f"256^bytes-1 ({max_val}). To convert this character, use "
                f"at least {needed_bytes} bytes."
            )  # pragma: no cover  Too difficult to test

        out = format(num, f"0{hex_chars}x") + out

    return out


def hex2str(hex_string, bytes_per_char=None):
    if not isinstance(hex_string, str):
        raise ValueError("Input must be a hexadecimal string.")

    defaults = settings.get_defaults()

    # defaults = {"bytes_per_char": 2, "max_bytes_per_char": 4}
    # Assuming these defaults

    bytes_per_char = bytes_per_char or defaults.bytes_per_char

    if (
        not isinstance(bytes_per_char, int)
        or bytes_per_char % 1 != 0
        or bytes_per_char < 1
        or bytes_per_char > defaults.max_bytes_per_char
    ):
        raise ValueError(
            f"Bytes per character must be an integer between 1 and "
            f"{defaults.max_bytes_per_char}, inclusive."
        )

    hex_chars = 2 * bytes_per_char

    # Pad left if necessary
    hex_string = hex_string.zfill(
        len(hex_string) + (hex_chars - len(hex_string) % hex_chars) % hex_chars
    )

    out = ""
    for i in range(0, len(hex_string), hex_chars):
        char_code = int(hex_string[i : i + hex_chars], 16)
        out = chr(char_code) + out

    return out


def getConfig():
    settings.update_defaults(hasCSPRNG=isSetRNG())
    return settings.get_config()


# # Core Functions from secrets.js
# init = jsFunction('init')
# combine = jsFunction('combine')
# getConfig = jsFunction('getConfig')
# extractShareComponents = jsFunction('extractShareComponents')
# setRNG = jsFunction('setRNG')
# str2hex = jsFunction('str2hex')
# hex2str = jsFunction('hex2str')
# random = jsFunction('random')
# share = jsFunction('share')
# newShare = jsFunction('newShare')
#
# # Test Functions
# _reset = jsNeedless('_reset')
# _isSetRNG = jsFunction('_isSetRNG')

#         /* test-code */
#         // export private functions so they can be unit tested directly.
#         _reset: reset,
#         _padLeft: padLeft,
#         _hex2bin: hex2bin,
#         _bin2hex: bin2hex,
#         _hasCryptoGetRandomValues: hasCryptoGetRandomValues,
#         _hasCryptoRandomBytes: hasCryptoRandomBytes,
#         _getRNG: getRNG,
#         _isSetRNG: isSetRNG,
#         _splitNumStringToIntArray: splitNumStringToIntArray,
#         _horner: horner,
#         _lagrange: lagrange,
#         _getShares: getShares,
#         _constructPublicShareString: constructPublicShareString
#         /* end-test-code */
