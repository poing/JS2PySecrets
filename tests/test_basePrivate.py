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
        faker.name(),
        faker.password(),
        faker.pystr(),
        faker.sentence(),
        faker.text(max_nb_chars=160),
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


def test_str2hex(random_string, bytes_per_char):
    # Convert random_string to bytes using specified encoding
    # byte_string = random_string.encode(encoding)

    # Perform conversion using str2hex function
    # string = str(byte_string)
    py_hex = secrets.str2hex(str(random_string), bytes_per_char)
    js_hex = node.str2hex(str(random_string), bytes_per_char)

    # Perform your assertions on hex_representation
    assert py_hex == js_hex


def test_str2hex_utf8():
    # Use the string from the JavaScript tests
    key = "¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹"

    # Perform conversion using str2hex function
    py_hex = secrets.str2hex(key)
    js_hex = node.str2hex(key)

    # Perform your assertions on hex_representation
    assert py_hex == js_hex


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


def test_hex2str(random_string, bytes_per_char):
    # Convert random_string to bytes using specified encoding
    # byte_string = random_string.encode(encoding)

    # Perform conversion using str2hex function
    py_hex = secrets.str2hex(str(random_string), bytes_per_char)
    js_hex = node.str2hex(str(random_string), bytes_per_char)

    # Perform your assertions on hex_representation
    assert py_hex == js_hex

    # Perform conversion using hex2str function py~py/js~js
    py_value = secrets.hex2str(py_hex, bytes_per_char)
    js_value = node.hex2str(js_hex, bytes_per_char)
    assert py_value == str(random_string)
    assert js_value == str(random_string)
    assert py_value == js_value

    # Perform conversion using hex2str function py~js/js~py
    py_string = secrets.hex2str(js_hex, bytes_per_char)
    js_string = node.hex2str(py_hex, bytes_per_char)
    assert py_string == str(random_string)
    assert js_string == str(random_string)
    assert py_string == js_string


def test_hex2str_input():
    match = "Input must be a hexadecimal string."
    with pytest.raises(ValueError, match=match):
        secrets.hex2str(1234)
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_hex2str_bytes():
    match = "must be an integer between 1 and 6"
    with pytest.raises(ValueError, match=match):
        string = secrets.str2hex("foobar")
        secrets.hex2str(string, 7)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
