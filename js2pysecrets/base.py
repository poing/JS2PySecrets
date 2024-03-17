# import json

# from .decorators import JsFunction, jsNeedless

# from .wrapper import wrapper  # Import your wrapper function

import math

from js2pysecrets.settings import Settings

NAME = "js2pysecrets"


settings = Settings()
# settings.update_defaults(rng=99)
# config = settings.get_config()


def reset():
    settings.reset_defaults()


def isSetRNG():
    if isinstance(settings.rng, str) or callable(settings.rng):
        return True
    return False


def padLeft(string, multipleOfBits=None):

    if multipleOfBits == 0 or multipleOfBits == 1:
        return string

    if multipleOfBits and multipleOfBits > 1024:
        raise ValueError(
            "Padding must be multiples of no larger than 1024 bits."
        )

    multipleOfBits = multipleOfBits or settings.bits

    if string:
        new_length = -(-len(string) // multipleOfBits) * multipleOfBits
        return string.zfill(new_length)

 

# def padLeft(string, multipleOfBits):
#     if multipleOfBits and isinstance(multipleOfBits, int)
# and multipleOfBits > 1:
#     multipleOfBits = multipleOfBits or settings.bits
#     return string.zfill(-(-len(str) // multipleOfBits) * multipleOfBits)


def bin2hex(binary_string: str) -> str:
    return hex(int(binary_string, 2))


def hex2bin(hex_string: str) -> str:
    return bin(int(hex_string, 16))


"""
ABOVE THIS LINE ARE INTERNAL FUNCTIONS
"""


def init(bits=None, rngType=None):
    logs = []
    exps = []
    x = 1
    primitive = None

    # reset all config back to initial state
    reset()

    if bits and (
        not isinstance(bits, int)
        or bits < settings.min_bits
        or bits > settings.max_bits
    ):
        raise ValueError(
            f"Number of bits must be an integer between {settings.min_bits} "
            f"and {settings.max_bits}, inclusive."
        )

    if rngType and not isinstance(rngType, str) or callable(rngType):
        raise ValueError(f"Invalid RNG type argument : '{rngType}'")

    settings.update_defaults(radix=settings.radix)
    settings.update_defaults(bits=bits or settings.bits)
    settings.update_defaults(size=(2**settings.bits))
    settings.update_defaults(maxShares=settings.size - 1)

    # Construct the exp and log tables for multiplication.
    primitive = settings.primitive_polynomials[settings.bits]

    for i in range(settings.size):
        exps.append(x)
        logs.append(i)
        x = x << 1  # Left shift assignment
        if x >= settings.size:
            x = x ^ primitive  # Bitwise XOR assignment
            x = x & settings.maxShares  # Bitwise AND assignment

    settings.update_defaults(logs=logs)
    settings.update_defaults(exps=exps)

    if rngType:
        settings.update_defaults(rng=rngType)

    if not isSetRNG():
        setRNG()  # pragma: no cover unlikely-and-redundant

    if (
        not isSetRNG()
        or not settings.bits
        or not settings.size
        or not settings.maxShares
        or not settings.logs
        or not settings.exps
        or len(settings.logs) != settings.size
        or len(settings.exps) != settings.size
    ):
        raise ValueError(
            "Initialization failed."
        )  # pragma: no cover hard-to-fail


"""
Adapted Python Random Number Generation:

This module provides a Python adaptation of the JavaScript code for random
number generation. It offers a minimalistic approach to replicating the
functionality present in the JavaScript version.

In the JavaScript version, supporting multiple RNGs was essential due to
differences in available random number generation mechanisms across different
environments. For example, Node.js provided `crypto.randomBytes()`, utilizing
OpenSSL's `RAND_bytes()` function, while browsers supported
`crypto.getRandomValues()`. Additionally, the `testRandom` function was
included for testing purposes, providing repeatable non-random bits.

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


def getRNG():
    if isinstance(settings.rng, str):
        return lambda bits: (bin(123456789)[2:].zfill(32) * -(-bits // 32))[
            -bits:
        ]
    return settings.rng


# lambda bits: bin(1+random.getrandbits(bits))[2:].zfill(bits)
# lambda bits: bin(1+secrets.randbits(bits))[2:].zfill(bits)
# lambda bits: (bin(123456789)[2:].zfill(32) * -(-bits // 32))[-bits:]
def setRNG(new_rng=None):
    defaults = settings.get_defaults()
    new_rng = new_rng or defaults.rng
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
