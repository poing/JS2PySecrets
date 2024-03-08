from js2pysecrets.decorators import JsFunction, jsNeedless
from js2pysecrets.wrapper import wrapper

import js2pysecrets.node as node
import pytest
import warnings


def not_supported(decorated_function):
    try:
        decorated_function()
        # If the function didn't raise an exception, return False
        return False
    except Exception as e:
        # If an exception was raised, ensure it matches the expected message
        expected_message = (
            "Calling subsequent JavaScript functions are not supported. -or- "
            "The JavaScript function isn't necessary for the Python version."
        )
        return str(e) == expected_message


@JsFunction
def invalidFunction(*args, **kwargs):
    pass


@jsNeedless
def needless(*args, **kwargs):
    pass  # pragma: no cover


def test_JsFunction():
    assert node.random(128) != node.random(32)


def test_jsNeedless():
    assert not_supported(lambda: needless(33, "blue"))


def test_Distinct():
    command = node.share("aabb", 6, 3, distinct=True)
    assert command == "share('aabb', 6, 3)"


def test_Randomness():
    count = 0
    num_trials = 10
    for _ in range(num_trials):
        # Simulate random behavior
        rand1 = node.random(16)
        rand2 = node.random(16)
        if int(rand1, 16) == int(rand2, 16):
            count += 1
    assert count < num_trials, "Randomness test failed"


def test_TestRNG():
    count = 0
    num_trials = 10
    for _ in range(num_trials):
        # Simulate random behavior
        rand1 = node.random(16, test=True)
        rand2 = node.random(16, test=True)
        if int(rand1, 16) == int(rand2, 16):
            count += 1
    assert count == num_trials, "Test RNG Failed"


@pytest.mark.filterwarnings("ignore:invalidFunction")
def test_invalidFunction():
    with warnings.catch_warnings(record=True) as caught_warnings:
        invalidFunction(1, 2, 3)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert "not a function" in str(caught_warnings[0].message)


@pytest.mark.filterwarnings("ignore:node.share")
def test_CalledProcessError():
    with warnings.catch_warnings(record=True) as caught_warnings:
        node.share("hello world", 3, 3)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert "Invalid hex character" in str(caught_warnings[0].message)


# @pytest.mark.filterwarnings("ignore:fail")
# def test_JSONDecodeError():
#     with warnings.catch_warnings(record=True) as caught_warnings:
#         node.fail()
#         # Check if any warnings were raised
#         assert len(caught_warnings) == 1
#         assert issubclass(caught_warnings[0].category, Warning)
#         assert "error decoding JSON" in str(caught_warnings[0].message)


# @pytest.mark.filterwarnings("ignore:wrapper")
# def test_JSONDecodeError():
#     with warnings.catch_warnings(record=True) as caught_warnings:
#         wrapper("hello world")
#         # Check if any warnings were raised
#         assert len(caught_warnings) == 1
#         assert issubclass(caught_warnings[0].category, Warning)
#         assert "error decoding JSON" in str(caught_warnings[0].message)
#         # assert True
