import js2pysecrets.base as secrets
import js2pysecrets.node as node
import pytest
from faker import Faker
import random
from js2pysecrets.settings import Settings
import warnings


settings = Settings()

# Initialize Faker with a seed for reproducibility
faker = Faker()


def test_isSetRNG():
    assert secrets.isSetRNG() == True
    secrets.setRNG("hello")
    assert secrets.isSetRNG() == True
    secrets.setRNG(1234)
    assert secrets.isSetRNG() == False


def test_get_config():
    settings.reset_defaults()
    py_config = secrets.getConfig()
    js_config = node.getConfig()
    assert py_config.radix == js_config["radix"]
    assert py_config.bits == js_config["bits"]
    assert py_config.maxShares == js_config["maxShares"]
    assert py_config.hasCSPRNG == js_config["hasCSPRNG"]
    assert py_config.typeCSPRNG != js_config["typeCSPRNG"]


@pytest.fixture(
    params=[
        faker.sentence(),
        faker.text(max_nb_chars=160),
        faker.pystr(),
        faker.password(),
        faker.name(),
        # Add more options as needed
    ]
)
def random_string(request):
    return request.param


@pytest.fixture(params=["ascii", "utf-8"])
def encoding(request):
    return request.param


@pytest.fixture(params=[None, 1, 2, 3, 4, 5, 6])
def bytes_per_char(request):
    return request.param


def test_str2hex(random_string, encoding, bytes_per_char):
    # Convert random_string to bytes using specified encoding
    byte_string = random_string.encode(encoding)

    # Perform conversion using str2hex function
    py_string = secrets.str2hex(str(byte_string), bytes_per_char)
    js_string = secrets.str2hex(str(byte_string), bytes_per_char)

    # Perform your assertions on hex_representation
    assert py_string == js_string


def test_str2hex_input():
    match = "Input must be a character string."
    with pytest.raises(ValueError, match=match):
        secrets.str2hex(1234)
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_str2hex_bytes():
    match = "must be an integer between 1 and 6"
    with pytest.raises(ValueError, match=match):
        secrets.str2hex("foobar", 7)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
