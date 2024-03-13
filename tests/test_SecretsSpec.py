#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

from js2pysecrets.wrapper import chain

import js2pysecrets.node as secrets
import pytest
import sys
import warnings


def test_withASCII():

    assert (
        secrets.hex2str(
            secrets.combine(secrets.share(secrets.str2hex("foo"), 3, 2))
        )
        == "foo"
    )


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="Windows default to CP-1252"
)
def test_with_UTF8():
    key = "¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹"
    expected = "\xa5 \xb7 \xa3 \xb7 \u20ac \xb7 $ \xb7 \xa2 \xb7 \u20a1 \xb7 \u20a2 \xb7 \u20a3 \xb7 \u20a4 \xb7 \u20a5 \xb7 \u20a6 \xb7 \u20a7 \xb7 \u20a8 \xb7 \u20a9 \xb7 \u20aa \xb7 \u20ab \xb7 \u20ad \xb7 \u20ae \xb7 \u20af \xb7 \u20b9"

    # Convert the key to UTF-8 bytes for comparison
    if sys.platform == "win32":
        key_bytes = key.encode("utf-8")
    else:
        key_bytes = key

    assert (
        secrets.hex2str(
            secrets.combine(secrets.share(secrets.str2hex(key_bytes), 3, 2))
        )
        == key
    )

    # .encode("utf-8", "strict")

    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))
        beforeEach.append(secrets.random(128, list=True))
        key = chain(beforeEach)[-1]

        # Test initialization with different arguments
        series = beforeEach.copy()

        # Test initialization with an empty argument
        series.append(secrets.getConfig(list=True))
        results = chain(series)
        assert results[-1]["bits"] == 8
        assert secrets.combine(secrets.share(key, 3, 2)) == key

        # Test initialization with an arg of 8
        series = beforeEach.copy()
        series.append(secrets.init(8, list=True))
        series.append(secrets.getConfig(list=True))
        results = chain(series)
        assert results[-1]["bits"] == 8
        assert secrets.combine(secrets.share(key, 3, 2)) == key

        # Test initialization with a min arg of 3
        series = beforeEach.copy()
        series.append(secrets.init(3, list=True))
        series.append(secrets.getConfig(list=True))
        results = chain(series)
        assert results[-1]["bits"] == 3
        assert secrets.combine(secrets.share(key, 3, 2)) == key

        # Test initialization with a max arg of 20
        series = beforeEach.copy()
        series.append(secrets.init(20, list=True))
        series.append(secrets.getConfig(list=True))
        series.append(secrets.share(key, 500, 2, list=True))
        results = chain(series)
        assert results[-2]["bits"] == 20
        shares = results[-1]
        # Specify a large number of shares for this test
        assert secrets.combine(shares) == key

        # Test initialization with a null arg
        series = beforeEach.copy()
        series.append(secrets.init(None, list=True))
        series.append(secrets.getConfig(list=True))
        results = chain(series)
        assert results[-1]["bits"] == 8
        assert secrets.combine(secrets.share(key, 3, 2)) == key

        # Test initialization with an undefined arg
        series = beforeEach.copy()
        series.append(secrets.init(list=True))
        series.append(secrets.getConfig(list=True))
        results = chain(series)
        assert results[-1]["bits"] == 8
        assert secrets.combine(secrets.share(key, 3, 2)) == key

        # Test initialization with a number less than 3
        series = beforeEach.copy()
        series.append(secrets.init(2, list=True))
        with warnings.catch_warnings(record=True) as caught_warnings:
            chain(series)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert "between 3 and 20" in str(caught_warnings[0].message)

        # Test initialization with a number greater than 20
        series = beforeEach.copy()
        series.append(secrets.init(21, list=True))
        with warnings.catch_warnings(record=True) as caught_warnings:
            chain(series)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert "between 3 and 20" in str(caught_warnings[0].message)


def test_getConfig():
    beforeEach = []

    # Define beforeEach to simulate JavaScript's beforeEach
    beforeEach.append(secrets.init(list=True))
    beforeEach.append(secrets.setRNG("testRandom", list=True))

    # Test getConfig with no args to init
    series = beforeEach.copy()
    series.append(secrets.getConfig(list=True))
    results = chain(series)
    assert results[-1] == {
        "radix": 16,
        "bits": 8,
        "maxShares": 255,
        "hasCSPRNG": True,
        "typeCSPRNG": "testRandom",
    }

    # Test getConfig with 16 bits arg to init
    series = beforeEach.copy()
    series.append(secrets.init(16, "testRandom", list=True))
    series.append(secrets.getConfig(list=True))
    results = chain(series)
    assert results[-1] == {
        "radix": 16,
        "bits": 16,
        "maxShares": 65535,
        "hasCSPRNG": True,
        "typeCSPRNG": "testRandom",
    }


"""
Random Number Generator Tests
setRNG with function test ommited
"""


def test_setRNG():
    beforeEach = []

    # Define beforeEach to simulate JavaScript's beforeEach
    beforeEach.append(secrets.init(list=True))
    beforeEach.append(secrets.setRNG("testRandom", list=True))

    # Test setRNG with valid type
    series = beforeEach.copy()
    series.append(secrets.setRNG("nodeCryptoRandomBytes", list=True))
    expected_type = "nodeCryptoRandomBytes"

    series.append(secrets.getConfig(list=True))
    results = chain(series)
    assert results[-1]["typeCSPRNG"] == expected_type

    #     # Test setRNG with function
    #     series = beforeEach.copy()
    #
    #     # Define the function to generate fixed-length strings of random digits
    #     def getFixedBitString(bits):
    #         return str(123456789)[:bits]
    #
    #     series.append(secrets.setRNG(getFixedBitString, list=True))
    #     # Expect the same random value every time since the fixed RNG always
    #     # returns the same string for a given bit length.
    #     expected_output = "123456789"
    #     assert secrets.random(128, list=True) == expected_output

    # Test setRNG with invalid type argument
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.setRNG("FOO")
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert "Invalid RNG type argument" in str(caught_warnings[0].message)

    #     # Test setRNG with function not returning string
    #     series = beforeEach.copy()
    #
    #     def getFixedBitStringNotString(bits):
    #         return ["not", "a", "string", str(bits)]
    #
    #     with pytest.raises(
    #         ValueError, match="Output is not a string. Supply an CSPRNG of the form function(bits){} that returns a string containing 'bits' number of random 1's and 0's."
    #     ):
    #         secrets.setRNG(getFixedBitStringNotString, list=True)

    #     # Test setRNG with function returning unparsable binary digits
    #     series = beforeEach.copy()
    #
    #     def getFixedBitStringInvalidOutput(bits):
    #         return "abcdef"
    #
    #     with pytest.raises(
    #         ValueError, match="Binary string output not parseable to an Integer. Supply an CSPRNG of the form function(bits){} that returns a string containing 'bits' number of random 1's and 0's."
    #     ):
    #         secrets.setRNG(getFixedBitStringInvalidOutput, list=True)

    #     # Test setRNG with function returning longer than config bits
    #     series = beforeEach.copy()
    #
    #     def getFixedBitStringLongOutput(bits):
    #         return "001010101"  # 9 when expecting 8
    #
    #     with pytest.raises(
    #         ValueError, match="Output length is greater than config.bits. Supply an CSPRNG of the form function(bits){} that returns a string containing 'bits' number of random 1's and 0's."
    #     ):
    #         secrets.setRNG(getFixedBitStringLongOutput, list=True)


#     # Test setRNG with function returning shorter than config bits
#     series = beforeEach.copy()
#
#     def getFixedBitStringShortOutput(bits):
#         return "0010101"  # 7 when expecting 8
#
#     with pytest.raises(
#         ValueError, match="Output length is less than config.bits. Supply an CSPRNG of the form function(bits){} that returns a string containing 'bits' number of random 1's and 0's."
#     ):
#         secrets.setRNG(getFixedBitStringShortOutput, list=True)


def test_share():
    beforeEach = []

    # Define beforeEach to simulate JavaScript's beforeEach
    beforeEach.append(secrets.init(list=True))
    beforeEach.append(secrets.setRNG("testRandom", list=True))

    # Test sharing into 'numShares' shares and retaining leading zeros where the key has leading zeros
    key = "000000000000000123"
    numShares = 10
    threshold = 5
    series = beforeEach.copy()
    series.append(secrets.share(key, numShares, threshold, list=True))
    results = chain(series)
    shares = results[-1]
    assert len(shares) == numShares
    assert secrets.combine(shares) == key

    # Test sharing into 'numShares' shares and retaining leading zeros where the key had leading zeros and was converted to hex
    key = "0000000 is the password"
    hex_key = secrets.str2hex(key)
    series = beforeEach.copy()
    series.append(secrets.share(hex_key, numShares, threshold, list=True))
    results = chain(series)
    shares = results[-1]
    assert len(shares) == numShares
    assert secrets.hex2str(secrets.combine(shares)) == key

    # Test sharing into 'numShares' shares where numShares is greater than the threshold
    series = beforeEach.copy()
    series.append(secrets.share(hex_key, numShares, threshold, list=True))
    results = chain(series)
    shares = results[-1]
    assert len(shares) > threshold

    # Test sharing into 'numShares' shares where numShares is equal to the threshold
    threshold = 10
    series = beforeEach.copy()
    series.append(secrets.share(hex_key, numShares, threshold, list=True))
    results = chain(series)
    shares = results[-1]
    assert len(shares) == numShares

    # Test sharing into 'numShares' shares where numShares is equal to the threshold and zero-padding is set
    series = beforeEach.copy()
    series.append(secrets.share(hex_key, numShares, threshold, list=True))
    series.append(
        secrets.share(hex_key, numShares, threshold, 1024, list=True)
    )
    results = chain(series)
    shares = results[-2]
    shares_with_zero_pad = results[-1]
    assert len(shares) == numShares
    assert len(shares_with_zero_pad) == numShares
    assert len(shares_with_zero_pad[0]) > len(shares[0])

    # Test for exceptions

    # Test sharing unless 'numShares' is less than the threshold
    numShares = 2
    threshold = 3
    match = "Threshold number of shares was 3 but must be less than or equal to the 2 shares specified as the total to generate."
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, numShares, threshold)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'numShares' is less than 2
    numShares = 1
    threshold = 2
    match = "Number of shares must be an integer between 2 and 2^bits-1 (255), inclusive."
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, numShares, threshold)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'numShares' is greater than 255
    numShares = 256
    threshold = 2
    match = "Number of shares must be an integer between 2 and 2^bits-1 (255), inclusive. To create 256 shares, use at least 9 bits."
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, numShares, threshold)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'threshold' is less than 2
    numShares = 2
    threshold = 1

    match = "Threshold number of shares must be an integer between 2 and 2^bits-1 (255), inclusive."

    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, numShares, threshold)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'threshold' is greater than 255
    numShares = 255
    threshold = 256

    match = "Threshold number of shares must be an integer between 2 and 2^bits-1 (255), inclusive.  To use a threshold of 256, use at least 9 bits."

    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, numShares, threshold)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'key' is not in the expected hex format
    key = "xyz123"
    match = "Invalid hex character."
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, 3, 2)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'key' is not a string
    key = {"foo": "bar"}
    match = "Unexpected template string"
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, 3, 2)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'padLength' is not a number
    match = "Unexpected template string"
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, 3, 2, "foo")
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'padLength' is not a whole number
    match = "Unexpected template string"
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, 3, 2, 1.3)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'padLength' is < 0
    match = "Unexpected template string"
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, 3, 2, -1)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)

    # Test sharing unless 'padLength' is > 1024
    match = "Unexpected template string"
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.share(key, 3, 2, 1025)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_combine_to_recreate_secret():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))
        beforeEach.append(secrets.random(128, list=True))
        key = chain(beforeEach)[-1]

        # Test initialization with different arguments
        series = beforeEach.copy()

        # Test initialization with an empty argument
        series.append(secrets.getConfig(list=True))
        results = chain(series)
        assert results[-1]["bits"] == 8
        assert secrets.combine(secrets.share(key, 3, 2)) == key

        known_key = "82585c749a3db7f73009d0d6107dd650"
        known_shares = [
            "80111001e523b02029c58aceebead70329000",
            "802eeb362b5be82beae3499f09bd7f9f19b1c",
            "803d5f7e5216d716a172ebe0af46ca81684f4",
            "804e1fa5670ee4c919ffd9f8c71f32a7bfbb0",
            "8050bd6ac05ceb3eeffcbbe251932ece37657",
            "8064bb52a3db02b1962ff879d32bc56de4455",
            "8078a5f11d20cbf8d907c1d295bbda1ee900a",
            "808808ff7fae45529eb13b1e9d78faeab435f",
            "809f3b0585740fd80830c355fa501a8057733",
            "80aeca744ec715290906c995aac371ed118c2",
        ]
        combined_key = secrets.combine(known_shares)
        assert combined_key == known_key

        series = beforeEach.copy()
        series.append(secrets.random(128, list=True))
        results = chain(series)
        key = results[-1]

        numShares = 10
        threshold = 5

        series = beforeEach.copy()
        series.append(secrets.share(key, numShares, threshold, list=True))
        results = chain(series)
        shares = results[-1]

        assert secrets.combine(shares) == key

        series = beforeEach.copy()
        series.append(secrets.share(key, 3, 2, 1024, list=True))
        results = chain(series)
        zero_pad_shares = results[-1]

        combined_key = secrets.combine(zero_pad_shares)
        assert combined_key == key

        combined_key = secrets.combine(shares + shares)
        assert combined_key == key

        combined_key = secrets.combine(shares[:threshold])
        assert combined_key == key

        combined_key = secrets.combine(shares[: threshold - 1])
        assert combined_key != key

        combined_key = secrets.combine([])
        assert combined_key != key

        combined_key = secrets.combine([])
        assert combined_key != key

        # FIXME: A cheater (imposter) share of the right format doesn't force failure.
        # series = beforeEach.copy()
        #         cheater_key = secrets.random(10)
        #         cheater_shares = secrets.share(cheater_key, 6, 2)
        #         shares.append(cheater_shares[3])
        #         combined_key = secrets.combine(shares)
        #         assert combined_key != key

        shares.append("abc123")
        match = "Invalid share : Share id must be an integer between 1 and 255, inclusive."
    with warnings.catch_warnings(record=True) as caught_warnings:
        secrets.combine(shares)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_generate_new_share():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))
        beforeEach.append(secrets.random(128, list=True))
        key = chain(beforeEach)[-1]

        # Test when newShare() is provided with only the minimum original shares required
        series = beforeEach.copy()
        series.append(secrets.share(key, 5, 2, list=True))
        results = chain(series)
        shares = results[-1]

        series = beforeEach.copy()
        series.append(secrets.newShare(6, shares[:2], list=True))
        results = chain(series)
        new_share = results[-1]

        parts = [shares[-2]]
        parts.append(new_share)

        combined_key = secrets.combine(parts)
        assert combined_key == key

        # Test combining mixed old/new shares back to the original key with ID arg as number
        series = beforeEach.copy()
        series.append(secrets.share(key, 3, 2, list=True))
        results = chain(series)
        shares = results[-1]

        series = beforeEach.copy()
        series.append(secrets.newShare(4, shares[:2], list=True))
        results = chain(series)
        new_share = results[-1]

        parts = [shares[-2]]
        parts.append(new_share)

        combined_key = secrets.combine(parts)
        assert combined_key == key

        # Test combining mixed old/new shares back to the original key with ID arg as string
        series = beforeEach.copy()
        series.append(secrets.share(key, 3, 2, list=True))
        results = chain(series)
        shares = results[-1]

        series = beforeEach.copy()
        fix = "4"  # Lint formater fix
        series.append(secrets.newShare(fix, shares[:2], list=True))
        results = chain(series)
        new_share = results[-1]

        parts = [shares[-2]]
        parts.append(new_share)

        combined_key = secrets.combine(parts)
        assert combined_key == key

        # Test combining mixed old/new shares back to the original key with ID arg as a float
        series = beforeEach.copy()
        series.append(secrets.share(key, 3, 2, list=True))
        results = chain(series)
        shares = results[-1]

        series = beforeEach.copy()
        series.append(secrets.newShare(1.3, shares[:2], list=True))
        results = chain(series)
        new_share = results[-1]

        parts = [shares[-2]]
        parts.append(new_share)

        combined_key = secrets.combine(parts)
        assert combined_key == key

        # Test unless ID arg is < 1
        series = beforeEach.copy()
        series.append(secrets.share(key, 3, 2, list=True))
        results = chain(series)
        shares = results[-1]

        series = beforeEach.copy()
        series.append(secrets.newShare(0, shares[:2], list=True))

        match = "Invalid 'id' or 'shares' Array argument to newShare()."
        with warnings.catch_warnings(record=True) as caught_warnings:
            results = chain(series)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless ID arg is > 255 for 8 bit config
        series = beforeEach.copy()
        series.append(secrets.share(key, 3, 2, list=True))
        results = chain(series)
        shares = results[-1]

        series = beforeEach.copy()
        series.append(secrets.newShare(256, shares[:2], list=True))

        match = "Share id must be an integer between 1 and 255, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            results = chain(series)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)


def test_round_trip_convert_string_to_hex_and_back():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))

        # Test if the string is plain ASCII text
        key = "acbdefghijklmnopqrstuvwxyz0123456789"
        series = beforeEach.copy()
        series.append(secrets.share(secrets.str2hex(key), 3, 2, list=True))
        results = chain(series)
        shares = results[-1]
        combined = secrets.combine(shares)
        combined_key = secrets.hex2str(combined)
        assert combined_key == key

        # Test if the string is UTF-8 text
        key = "¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹"
        series = beforeEach.copy()
        series.append(secrets.share(secrets.str2hex(key), 3, 2, list=True))
        results = chain(series)
        shares = results[-1]
        combined = secrets.combine(shares)
        combined_key = secrets.hex2str(combined)
        assert combined_key == key

        # Test if the string is UTF-16 text
        key = "𐑡𐑹𐑡 ·𐑚𐑻𐑯𐑸𐑛 ·𐑖𐑷"
        series = beforeEach.copy()
        series.append(secrets.share(secrets.str2hex(key), 3, 2, list=True))
        results = chain(series)
        shares = results[-1]
        combined = secrets.combine(shares)
        combined_key = secrets.hex2str(combined)
        assert combined_key == key

        # Test unless str2hex is called with a non-string
        match = "Input must be a character string."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.str2hex([])
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless str2hex bytesPerChar arg is non-Integer
        match = "Bytes per character must be an integer between 1 and 6, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.str2hex("abc", "foo")
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless str2hex bytesPerChar arg is < 1
        match = "Bytes per character must be an integer between 1 and 6, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.str2hex("abc", -1)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless str2hex bytesPerChar arg is > 6
        match = "Bytes per character must be an integer between 1 and 6, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.str2hex("abc", 7)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless hex2str is called with a non-string
        match = "Input must be a hexadecimal string."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.hex2str([])
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless hex2str bytesPerChar arg is non-Integer
        match = "Bytes per character must be an integer between 1 and 6, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.hex2str("abc", "foo")
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless hex2str bytesPerChar arg is < 1
        match = "Bytes per character must be an integer between 1 and 6, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.hex2str("abc", -1)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless hex2str bytesPerChar arg is > 6
        match = "Bytes per character must be an integer between 1 and 6, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.hex2str("abc", 7)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)


def test_generate_random_hex_string():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))

        # Test with valid Hex chars 0-9 and a-f
        series = beforeEach.copy()
        series.append(secrets.random(128, list=True))
        rnd = chain(series)[-1]
        assert all(char in "0123456789abcdef" for char in rnd)

        # Test of 2 bit length
        series = beforeEach.copy()
        series.append(secrets.random(2, list=True))
        rnd = chain(series)[-1]
        assert len(rnd) == 1

        # Test of 128 bit length
        series = beforeEach.copy()
        series.append(secrets.random(128, list=True))
        rnd = chain(series)[-1]
        assert len(rnd) == 32

        # Test of 512 bit length
        series = beforeEach.copy()
        series.append(secrets.random(512, list=True))
        rnd = chain(series)[-1]
        assert len(rnd) == 128

        # Test unless bitlength is less than 2
        match = "Number of bits must be an Integer between 1 and 65536."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.random(1)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless bitlength is greater than than 65536
        match = "Number of bits must be an Integer between 1 and 65536."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.random(65537)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)


def test_conversion_functions():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))

        # Test from a known binary string to a known hex output
        binStr = "00110101110001100110001011011111111100110000011111110000010010010011101001000000111010001111000111001110011000011101111111011111010111100111011100110101010000110110010101110010110101010101100000110010000010001000110101110010011110100111001010010100011001110110001010000000110000111110011100101111111110100001011100000110000101101000011100101000000100000111001010110100011001110100110001000010000011101100001111100011001001110101101100101011011101010110010100010110111000001010000000001110000010110100000010111101"
        hexOutput = "35c662dff307f0493a40e8f1ce61dfdf5e7735436572d55832088d727a7294676280c3e72ffa17061687281072b4674c420ec3e3275b2b756516e0a00e0b40bd"
        assert secrets._bin2hex(binStr) == hexOutput

        # Test from a known hex string to a known binary output
        hexStr = "35c662dff307f0493a40e8f1ce61dfdf5e7735436572d55832088d727a7294676280c3e72ffa17061687281072b4674c420ec3e3275b2b756516e0a00e0b40bd"
        binOutput = "00110101110001100110001011011111111100110000011111110000010010010011101001000000111010001111000111001110011000011101111111011111010111100111011100110101010000110110010101110010110101010101100000110010000010001000110101110010011110100111001010010100011001110110001010000000110000111110011100101111111110100001011100000110000101101000011100101000000100000111001010110100011001110100110001000010000011101100001111100011001001110101101100101011011101010110010100010110111000001010000000001110000010110100000010111101"
        assert secrets._hex2bin(hexStr) == binOutput

        # Test from a known ASCII String > Hex > Binary > Hex > ASCII String round trip
        strInput = "I want to play safely!"
        hexStr = secrets.str2hex(strInput)
        binStr = secrets._hex2bin(hexStr)
        hexStr2 = secrets._bin2hex(binStr)
        assert secrets.hex2str(hexStr2) == strInput

        # Test from a known UTF-8 String > Hex > Binary > Hex > UTF-8 String round trip
        strInput = "¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹"
        hexStr = secrets.str2hex(strInput)
        binStr = secrets._hex2bin(hexStr)
        hexStr2 = secrets._bin2hex(binStr)
        assert secrets.hex2str(hexStr2) == strInput

        # Test from a known UTF-16 String > Hex > Binary > Hex > UTF-16 String round trip
        strInput = "𐑡𐑹𐑡 ·𐑚𐑻𐑯𐑸𐑛 ·𐑖𐑷"
        hexStr = secrets.str2hex(strInput)
        binStr = secrets._hex2bin(hexStr)
        hexStr2 = secrets._bin2hex(binStr)
        assert secrets.hex2str(hexStr2) == strInput

        # Test unless a non binary character is passed to bin2hex
        match = "Invalid binary character."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets._bin2hex("000100019999")
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)


def test_extract_share_data():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))

        # Test when 8 bit shares are created
        shares_8_bit = [
            "8013ac6c71ce163b661fa6ac8ce0141885ebee425222f1f07d07cad2e4a63f995b7",
            "80274919338dfc671c2e9d78d2e02140d0d61624a245ea20e0ff8e45c0dc68f37a8",
            "8034e5754243ea5c7a313bc45850327853cdfeb6f2671c909b184287230a556a256",
        ]
        data = [
            "3ac6c71ce163b661fa6ac8ce0141885ebee425222f1f07d07cad2e4a63f995b7",
            "74919338dfc671c2e9d78d2e02140d0d61624a245ea20e0ff8e45c0dc68f37a8",
            "4e5754243ea5c7a313bc45850327853cdfeb6f2671c909b184287230a556a256",
        ]

        for i, share in enumerate(shares_8_bit, start=1):
            share_components = secrets.extractShareComponents(share)
            assert share_components["bits"] == 8
            assert share_components["id"] == i
            assert share_components["data"] == data[i - 1]

        # Test when 1000 20 bit shares are created
        share_20_bit = "K003e88f72b74da4a55404d3abd1dc9a44199d50fd27e79cf974633fe1eae164d91b022"
        data = (
            "8f72b74da4a55404d3abd1dc9a44199d50fd27e79cf974633fe1eae164d91b022"
        )
        share_components = secrets.extractShareComponents(share_20_bit)
        assert share_components["bits"] == 20
        assert share_components["id"] == 1000
        assert share_components["data"] == data

        # Test when 20 bit shares are created
        shares_20_bit = [
            "K000019359d6ab1e44238b75ef84d1cba6e16b4c36ba325d539c82cb147403c8765c951",
            "K0000226b33d563c884706ebd739a9e744abdd88660462baaee90ebf22d80e00eab9279",
            "K00003b5eaebfd22cc648d9e38ad7e7ce56ab034566e52e7fa358a9430bc0ab89ee5b61",
        ]

        data = [
            "9359d6ab1e44238b75ef84d1cba6e16b4c36ba325d539c82cb147403c8765c951",
            "26b33d563c884706ebd739a9e744abdd88660462baaee90ebf22d80e00eab9279",
            "b5eaebfd22cc648d9e38ad7e7ce56ab034566e52e7fa358a9430bc0ab89ee5b61",
        ]

        for i, share in enumerate(shares_20_bit, start=1):
            share_components = secrets.extractShareComponents(share)
            assert share_components["bits"] == 20
            assert share_components["id"] == i
            assert share_components["data"] == data[i - 1]

        # Test unless the share is in an invalid format
        match = "Invalid share : Number of bits must be an integer between 3 and 20, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets.extractShareComponents("Zabc123")
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)
