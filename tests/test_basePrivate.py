from faker import Faker
from js2pysecrets.decorators import JsFunction
from js2pysecrets.settings import Settings
import js2pysecrets.base as secrets
import js2pysecrets.node as node
import pytest
import random
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


def test_str2hex_ASCII():
    # Set the test string
    test_string = "foobar"

    # Perform conversion using the str2hex function in Python
    py_hex = secrets.str2hex(test_string)

    # Perform conversion using the str2hex function in JavaScript
    js_hex = node.str2hex(test_string)

    # Confirm the Python and JavaScript outputs match
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


def test_init():
    secrets.init(10, "hello world")
    assert settings.bits == 10
    assert settings.rng == "hello world"


def test_init_min():
    match = "Number of bits must be an integer between"
    with pytest.raises(ValueError, match=match):
        secrets.init(2)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_init_max():
    match = "Number of bits must be an integer between"
    with pytest.raises(ValueError, match=match):
        secrets.init(21)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_init_RNG():
    match = "Invalid RNG type"
    with pytest.raises(ValueError, match=match):
        secrets.init(8, 1234)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


@JsFunction
def binNodeCryptoRandomBytes(*args, **kwargs):
    pass  # pragma: no cover


@JsFunction
def binTestRandom(*args, **kwargs):
    pass  # pragma: no cover


def test_node_bin_nodeCryptoRandomBytes():
    count = 0
    num_trials = 10
    for _ in range(num_trials):
        # Simulate random behavior
        rand1 = binNodeCryptoRandomBytes(16)
        rand2 = binNodeCryptoRandomBytes(16)
        if int(rand1, 16) == int(rand2, 16):
            count += 1
    assert count < num_trials, "Randomness test failed"


def test_node_bin_testRandom():
    count = 0
    num_trials = 10
    for _ in range(num_trials):
        # Simulate random behavior
        rand1 = binTestRandom(16)
        rand2 = binTestRandom(16)
        if int(rand1, 16) == int(rand2, 16):
            count += 1
    assert count == num_trials, "Test Keyword Failed"
    assert rand1 == "1100110100010101"
    assert rand2 == "1100110100010101"


def test_init_RNG():
    match = "Invalid RNG type"
    with pytest.raises(ValueError, match=match):
        secrets.init(8, 1234)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def bit_range(input_range):
    block_size = int(2048 / (input_range + 1))
    bits = (block_size * (input_range + 1)) - random.randrange(0, block_size)
    return bits


@pytest.mark.parametrize("input_range", range(random.randrange(1, 2047)))
def test_getRNG(input_range):
    bits = bit_range(input_range)
    secrets.init()
    secrets.setRNG("testRandom")
    assert secrets.isSetRNG() == True
    py_random = secrets.getRNG()
    assert len(py_random(bits)) == bits
    assert len(py_random(bits)) == len(py_random(bits))
    assert py_random(bits) == py_random(bits)
    assert py_random(bits) != py_random(bits + 1)


@pytest.mark.parametrize("input_range", range(random.randrange(1, 2047)))
def test_node_py_getRNG(input_range):
    # block_size = int(2048 / (input_range + 1))
    # bits = (block_size * (input_range + 1)) - random.randrange(0, block_size)
    bits = bit_range(input_range)
    secrets.init()
    secrets.setRNG("testRandom")
    assert secrets.isSetRNG() == True
    py_command = secrets.getRNG()
    py_random = py_command(bits)
    js_random = binTestRandom(bits)
    assert py_random == js_random
    assert len(py_random) == bits
    assert len(js_random) == bits
    assert len(py_random) == len(js_random)


@pytest.mark.parametrize("input_range", range(random.randrange(1, 2047)))
def test_node_py_lengthRNG(input_range):
    # block_size = int(2048 / (input_range + 1))
    # bits = (block_size * (input_range + 1)) - random.randrange(0, block_size)
    bits = bit_range(input_range)
    secrets.init()
    assert secrets.isSetRNG() == True
    py_command = secrets.getRNG()
    py_random = py_command(bits)
    js_random = binTestRandom(bits)

    secrets.init()
    assert secrets.isSetRNG() == True
    secrets.setRNG("testRandom")
    py_command = secrets.getRNG()
    py_test = py_command(bits)
    js_test = binNodeCryptoRandomBytes(bits)
    assert (
        len(py_random)
        == len(js_random)
        == len(py_test)
        == len(js_test)
        == bits
    )


@pytest.fixture(
    params=[
        2,
        3,
        5,
        7,
        11,
        13,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
        67,
        71,
        73,
        79,
        83,
        89,
        97,
        101,
        103,
        107,
        109,
        113,
        127,
        131,
        137,
        139,
        149,
        151,
        157,
        163,
        167,
        173,
        179,
        181,
        191,
        193,
        197,
        199,
        211,
        223,
        227,
        229,
        233,
        239,
        241,
        251,
        257,
        263,
        269,
        271,
        277,
        281,
        283,
        293,
        307,
        311,
        313,
        317,
        331,
        337,
        347,
        349,
        353,
        359,
        367,
        373,
        379,
        383,
        389,
        397,
        401,
        409,
        419,
        421,
        431,
        433,
        439,
        443,
        449,
        457,
        461,
        463,
        467,
        479,
        487,
        491,
        499,
        503,
        509,
        521,
        523,
        541,
        547,
        557,
        563,
        569,
        571,
        577,
        587,
        593,
        599,
        601,
        607,
        613,
        617,
        619,
        631,
        641,
        643,
        647,
        653,
        659,
        661,
        673,
        677,
        683,
        691,
        701,
        709,
        719,
        727,
        733,
        739,
        743,
        751,
        757,
        761,
        769,
        773,
        787,
        797,
        809,
        811,
        821,
        823,
        827,
        829,
        839,
        853,
        857,
        859,
        863,
        877,
        881,
        883,
        887,
        907,
        911,
        919,
        929,
        937,
        941,
        947,
        953,
        967,
        971,
        977,
        983,
        991,
        997,
        1009,
        1013,
        1019,
        1021,
    ]
)
def prime_numbers(request):
    return request.param


@pytest.fixture(params=[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
def multiple_numbers(request):
    return request.param


def test_node_py_padLeft_spotCheck():
    py_command = secrets.getRNG()
    py_random = py_command(11)
    # py_string = secrets.padLeft(py_random, multiple_numbers)
    # js_string = node._padLeft(py_random, multiple_numbers)
    assert len(secrets.padLeft(py_random, 0)) == 11
    assert len(secrets.padLeft(py_random, 1)) == 11
    assert len(secrets.padLeft(py_random, 3)) == 12
    assert len(secrets.padLeft(py_random, 5)) == 15
    assert len(secrets.padLeft(py_random, 7)) == 14
    assert len(secrets.padLeft(py_random, 8)) == 16
    assert len(secrets.padLeft(py_random, 9)) == 18
    assert len(secrets.padLeft(py_random, 10)) == 20


def test_node_py_padLeft(prime_numbers, multiple_numbers):
    py_command = secrets.getRNG()
    py_random = py_command(prime_numbers)
    py_string = secrets.padLeft(py_random, multiple_numbers)
    js_string = node._padLeft(py_random, multiple_numbers)
    assert py_string == js_string
    assert len(py_string) == len(js_string)
    assert (len(py_string) % multiple_numbers) == 0
    assert (len(js_string) % multiple_numbers) == 0
