import js2pysecrets.node as node
import warnings
import pytest


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


def test_init():
    assert not_supported(lambda: node.init(33))


def test_newShare():
    assert not_supported(lambda: node.newShare(33, "blue"))


def test_random():
    def test_random_behavior(self):
        count = 0
        num_trials = 1000
        for _ in range(num_trials):
            # Simulate random behavior
            rand1 = node.random(1)
            rand2 = node.random(1)
            if rand1 != rand2:
                count += 1

        probability = count / num_trials
        # Check if the probability is within a reasonable range
        assert 0.2 < probability < 0.8, "Randomness test failed"


def test_anotherRand():
    assert node.random(128) != node.random(128)


def test_testRand():
    alpha = node.random(10, test=True)
    bravo = node.random(10, test=True)
    assert alpha == bravo


from js2pysecrets.decorators import JsFunction


@JsFunction
def invalidFunction(*args, **kwargs):
    pass


@pytest.mark.filterwarnings("ignore:broken")
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


@pytest.mark.filterwarnings("ignore:node.combine")
def test_JSONDecodeError():
    with warnings.catch_warnings(record=True) as caught_warnings:
        node.combine()
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert "error decoding JSON" in str(caught_warnings[0].message)
