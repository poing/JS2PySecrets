#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:

from js2pysecrets.wrapper import chain

import js2pysecrets.node as secrets
import pytest
import sys
import warnings


def test_pad_left():
    with warnings.catch_warnings(record=True) as caught_warnings:
        beforeEach = []

        # Define beforeEach to simulate JavaScript's beforeEach
        beforeEach.append(secrets.init(list=True))
        beforeEach.append(secrets.setRNG("testRandom", list=True))

        # Test without specifying bits of padding it should default to config.bits
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        str_value = "abc123"
        series.append(secrets._padLeft(str_value, list=True))

        results = chain(series)
        padded_value = results[-1]
        assert padded_value == "0000abc123"
        assert len(padded_value) == 10

        # Test with null bits of padding it should default to config.bits
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        series.append(secrets._padLeft(str_value, None, list=True))
        results = chain(series)
        padded_value_null = results[-1]
        assert padded_value_null == "0000abc123"
        assert len(padded_value_null) == 10

        # Test with zero bits of padding
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        series.append(secrets._padLeft(str_value, 0, list=True))
        results = chain(series)
        padded_value_zero = results[-1]

        assert padded_value_zero == str_value
        assert len(padded_value_zero) == 6

        # Test with 1 bit of padding
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        series.append(secrets._padLeft(str_value, 1, list=True))
        results = chain(series)
        padded_value_one = results[-1]

        assert padded_value_one == str_value
        assert len(padded_value_one) == 6

        # Test with a value that is shorter than bits
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        str_value_short = "abc123"
        series.append(secrets._padLeft(str_value_short, 32, list=True))
        results = chain(series)

        padded_value_short = results[-1]
        assert padded_value_short == "00000000000000000000000000abc123"
        assert len(padded_value_short) == 32

        # Test with a value that is equal in size to bits
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        str_value_equal = "01234567890123456789012345678901"
        series.append(secrets._padLeft(str_value_equal, 32, list=True))
        results = chain(series)

        padded_value_equal = results[-1]
        assert padded_value_equal == str_value_equal
        assert len(padded_value_equal) == 32

        # Test with a value that is larger than bits
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        str_value_large = "0123456789012345678901234567890123456789"
        series.append(secrets._padLeft(str_value_large, 32, list=True))
        results = chain(series)

        padded_value_large = results[-1]
        assert (
            padded_value_large
            == "0000000000000000000000000123456789012345678901234567890123456789"
        )
        assert len(padded_value_large) == 64

        # Test with bits set to the max of 1024
        series = beforeEach.copy()
        series.append(secrets.init(10, list=True))

        series.append(secrets._padLeft(str_value_large, 1024, list=True))
        results = chain(series)

        padded_value_max = results[-1]
        assert len(padded_value_max) == 1024

        # Test unless bits set greater than the max of 1024
        match = "Padding must be multiples of no larger than 1024 bits."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets._padLeft("abc123", 1025)
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)


def test_construct_public_share_string():
    with warnings.catch_warnings(record=True) as caught_warnings:
        # Test should construct a well formed 3 bit share
        assert secrets._constructPublicShareString(3, 1, "ffff") == "31ffff"

        # Test should construct a well formed 8 bit share
        assert secrets._constructPublicShareString(8, 1, "ffff") == "801ffff"

        # Test should construct a well formed 20 bit share
        assert (
            secrets._constructPublicShareString(20, 1024, "ffff")
            == "K01024ffff"
        )

        # Test should construct a well formed 20 bit share with bits as a string
        assert (
            secrets._constructPublicShareString("20", 1024, "ffff")
            == "K01024ffff"
        )

        # Test should construct a well formed 20 bit share with ID as a string
        assert (
            secrets._constructPublicShareString(20, "1024", "ffff")
            == "K01024ffff"
        )

        # Test unless id < 1
        match = "Share id must be an integer between 1 and 255, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets._constructPublicShareString(8, 0, "ffff")
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)

        # Test unless id > 255
        match = "Share id must be an integer between 1 and 255, inclusive."
        with warnings.catch_warnings(record=True) as caught_warnings:
            secrets._constructPublicShareString(8, 256, "ffff")
            # Check if any warnings were raised
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert match in str(caught_warnings[0].message)
