import math
import re

from js2pysecrets.settings import Settings

NAME = "js2pysecrets"


settings = Settings()


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


def bin2hex(binary_string: str) -> str:
    hex_string = hex(int(binary_string, 2))[2:]

    # Need to respect any leading zeros in the binary string when converting
    #  to hex.  Because 0b0011 = 0x3, while 0x03 is desired
    hex_string = hex_string.zfill((len(padLeft(binary_string, 4)) // 4))

    return hex_string


def hex2bin(hex_str):
    bin_str = ""

    # Can NOT use `bin(int(hex_str, 16))[2:]` for this conversion.  Need to
    #  use this unconventional method to match the JavaScript, specifically
    #  to achieve the correct zero padding in the binary string output.
    for char in reversed(hex_str):
        try:
            num = int(char, 16)
        except ValueError:
            raise ValueError(f"Invalid hex character: {char}")

        bin_str = bin(num)[2:].zfill(4) + bin_str

    return bin_str


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
it will function like the JavaScript `testRandom` RNG for testing purposes.

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


def hasCryptoGetRandomValues():
    # Browser supports crypto.getRandomValues()
    # Depreciated - Not Applicable for Python Version
    return False  # pragma: no cover


def hasCryptoRandomBytes():
    # Node.js support for crypto.randomBytes()
    # Depreciated - Not Applicable for Python Version
    return False  # pragma: no cover


def getRNG():
    if isinstance(settings.rng, str):
        return lambda bits: (bin(123456789)[2:].zfill(32) * -(-bits // 32))[
            -bits:
        ]
    return settings.rng


def splitNumStringToIntArray(string, pad_length=None):
    parts = []

    if pad_length:
        string = padLeft(string, pad_length)

    # Reverse the string to facilitate right-to-left splitting
    string = string[::-1]

    for i in range(0, len(string), settings.bits):
        # print(string[i : i + settings.bits][::-1])
        parts.append(int(string[i : i + settings.bits][::-1], 2))

    return parts


# Horner's method for polynomial evaluation.
def horner(x, coeffs):

    logx = settings.logs[x]
    fx = 0

    for i in range(len(coeffs) - 1, -1, -1):
        if fx != 0:

            fx = (
                settings.exps[(logx + settings.logs[fx]) % settings.maxShares]
                ^ coeffs[i]
            )

        else:
            fx = coeffs[i]

    return fx


# Lagrange interpolation formula for polynomial interpolation
def lagrange(at, x, y):
    result = 0
    length = len(x)

    for i in range(length):
        if y[i]:
            product = settings.logs[y[i]]

            for j in range(length):
                if i != j:
                    if at == x[j]:
                        product = -1  # pragma: no cover
                        break  # pragma: no cover

                    product = (
                        product
                        + settings.logs[at ^ x[j]]
                        - settings.logs[x[i] ^ x[j]]
                        + settings.maxShares
                    ) % settings.maxShares

            result = (
                result ^ settings.exps[product] if product != -1 else result
            )

    return result


def getShares(secret, num_shares, threshold):
    shares = []
    coeffs = [secret]

    rng = getRNG()

    for i in range(1, threshold):

        # Generate non-zero random number
        random_number = rng(settings.bits)
        while int(random_number, 2) < 0:
            random_number = rng(settings.bits)  # pragma: no cover

        # Check if dithering function is specified and callable, this captures
        # the random data using the provided function for dithering or similar
        # auditing purposes.
        if settings.dithering and callable(settings.dithering):
            capture = settings.dithering
            capture(random_number)

        coeffs.append(int(random_number, 2))

    for i in range(1, num_shares + 1):
        shares.append({"x": i, "y": horner(i, coeffs)})

    return shares


def constructPublicShareString(bits, share_id, data):

    def base36encode(
        number, alphabet="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ):  # pragma: no cover
        """Converts an integer to a base36 string."""
        if not isinstance(number, int):
            raise TypeError("number must be an integer")

        base36 = ""
        sign = ""

        if number < 0:
            sign = "-"
            number = -number

        if 0 <= number < len(alphabet):
            return sign + alphabet[number]

        while number != 0:
            number, i = divmod(number, len(alphabet))
            base36 = alphabet[i] + base36

        return sign + base36

    share_id = int(share_id, 10)  # Value is stored as int
    bits = bits or settings.bits
    bits_base36 = base36encode(bits).upper()
    id_max = settings.maxShares
    id_padding_len = len(hex(int(id_max))[2:])
    id_hex = padLeft(hex(int(share_id))[2:], id_padding_len)

    if not (
        isinstance(share_id, int)
        and share_id % 1 == 0
        and 1 <= share_id <= id_max
    ):
        raise ValueError(
            f"Share id must be an integer between 1 and {id_max}, inclusive."
        )  # pragma: no cover

    new_share_string = bits_base36 + id_hex + data

    return new_share_string


"""
ABOVE THIS LINE ARE INTERNAL FUNCTIONS
"""


def init(bits=None, rngType=None):
    exps = []
    logs = [None]
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

    temp_logs = {}  # Temporary Dict to hold indexed logs
    for i in range(settings.size):
        # this works with loop below
        exps.insert(i, x)
        temp_logs[x] = i

        x = x << 1  # Left shift assignment
        if x >= settings.size:
            x = x ^ primitive  # Bitwise XOR assignment
            x = x & settings.maxShares  # Bitwise AND assignment

    # Fill the logs List in the proper order
    for i in range(1, settings.size):
        logs.append(temp_logs[i])

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


def combine(shares, at=0):
    result = ""
    set_bits = None
    x = []
    y = []

    at = at or 0

    for share in shares:
        share_components = extractShareComponents(share)
        share_id = share_components["id"]
        share_data = share_components["data"]

        # All shares must have the same bits settings.
        if set_bits is None:
            set_bits = share_components["bits"]
        elif set_bits != share_components["bits"]:
            raise ValueError("Mismatched shares: Different bit settings.")

        # Reset everything to the bit settings of the shares.
        if settings.bits != set_bits:
            init(set_bits)

        # Gathering all the provided shares
        if share_id not in x:
            x.append(share_id)
            split_share = splitNumStringToIntArray(hex2bin(share_data))
            y.append(split_share)

    # Zipping all of the shares together.
    y = list(zip(*y))

    # Extract the secret from the 'rotated' share data and return a
    # string of Binary digits which represent the secret directly. or in the
    # case of a newShare() return the binary string representing just that
    # new share.
    for yi in y:

        result = padLeft(bin(lagrange(at, x, yi))[2:]) + result

    return (
        bin2hex(result) if at >= 1 else bin2hex(result[result.find("1") + 1 :])
    )


def getConfig():
    settings.update_defaults(hasCSPRNG=isSetRNG())
    return settings.get_config()


def extractShareComponents(share):

    defaults = {
        "minBits": 1,
        "maxBits": 32,
    }  # Assuming defaults for minBits and maxBits

    config = {"radix": 16}  # Assuming radix as 16 for hex numbers
    bits = int(share[0], 36)

    if not (
        bits
        and isinstance(bits, int)
        and bits % 1 == 0
        and defaults["minBits"] <= bits <= defaults["maxBits"]
    ):
        raise ValueError(
            f"Invalid share: Number of bits must be an integer between "
            f"{settings.min_bits} and {settings.max_bits}, inclusive."
        )  # pragma: no cover

    max_shares = 2**bits - 1
    id_len = len(hex(max_shares)[2:])

    regex_str = (
        "^([a-kA-K3-9]{1})([a-fA-F0-9]{" + str(id_len) + "})([a-fA-F0-9]+)$"
    )
    share_components = re.match(regex_str, share)

    if share_components:
        share_id = int(share_components.group(2), config["radix"])
        if not (
            isinstance(share_id, int)
            and share_id % 1 == 0
            and 1 <= share_id <= max_shares
        ):
            raise ValueError(
                f"Invalid share: Share id must be an integer between 1 and "
                f"{max_shares}, inclusive."
            )  # pragma: no cover

        return {
            "bits": bits,
            "id": share_id,
            "data": share_components.group(3),
        }

    raise ValueError("Invalid share data provided.")


# lambda bits: bin(random.getrandbits(bits))[2:].zfill(bits)
# lambda bits: bin(secrets.randbits(bits))[2:].zfill(bits)
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


def random(bits):

    if not isinstance(bits, int) or bits < 2 or bits > 65536:
        raise ValueError(
            "Number of bits must be an Integer between 2 and 65536."
        )

    rng = getRNG()

    return bin2hex(rng(bits))


def share(secret, num_shares, threshold, pad_length=None):

    # Security: pad in multiples of 128 bits by default
    pad_length = pad_length or 128

    if not isinstance(secret, str) or not all(
        c in "0123456789abcdefABCDEF" for c in secret
    ):
        raise ValueError("Secret must be a hex string.")

    if not isinstance(num_shares, int) or num_shares <= 2:
        raise ValueError("Number of shares must be an integer >= 2.")

    if num_shares > settings.maxShares:
        needed_bits = math.ceil(math.log(num_shares + 1) / math.log(2))
        raise ValueError(
            f"Number of shares must be <= {settings.maxShares}."
            f" Use at least {needed_bits} bits."
        )

    if not isinstance(threshold, int) or threshold < 2:
        raise ValueError("Threshold number of shares must be an integer >= 2.")

    if threshold > settings.maxShares:
        needed_bits = math.ceil(math.log(threshold + 1) / math.log(2))
        raise ValueError(
            f"Threshold number of shares must be <= "
            f"{settings.maxShares}. Use at least {needed_bits} bits."
        )

    if threshold > num_shares:
        raise ValueError(
            "Threshold number of shares must be less than or equal to the "
            "total shares specified."
        )

    if not isinstance(pad_length, int) or pad_length < 0 or pad_length > 1024:
        raise ValueError(
            "Zero-pad length must be an integer between 0 and 1024 inclusive."
        )

    secret = "1" + hex2bin(secret)  # prepend a 1 as a marker

    secret = splitNumStringToIntArray(secret, pad_length)

    num_shares = int(num_shares)
    threshold = int(threshold)

    x = [None] * num_shares
    y = [None] * num_shares

    for i in range(len(secret)):
        sub_shares = getShares(secret[i], num_shares, threshold)
        for j in range(num_shares):
            x[j] = x[j] or str(sub_shares[j]["x"])
            y[j] = padLeft(bin(sub_shares[j]["y"])[2:]) + (y[j] or "")

    for i in range(num_shares):
        x[i] = constructPublicShareString(settings.bits, x[i], bin2hex(y[i]))

    return x


def newShare(id, shares):
    if id and isinstance(id, str):
        id = int(id, settings.radix)  # pragma: no cover

    radid = str(id)

    if id and radid and shares and shares[0]:
        # share = extractShareComponents(shares[0])
        return constructPublicShareString(
            settings.bits, radid, combine(shares, id)
        )

    raise ValueError(
        "Invalid 'id' or 'shares' Array argument to newShare()."
    )  # pragma: no cover
