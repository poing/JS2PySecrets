from faker import Faker
from js2pysecrets.decorators import JsFunction
from js2pysecrets.settings import Settings
import js2pysecrets.base as secrets
import js2pysecrets.node as node
import pytest
import random
import warnings
from js2pysecrets.wrapper import wrapper, chain


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


def test_padLeft_Fail():
    match = "Padding must be multiples of no larger than 1024 bits."
    with pytest.raises(ValueError, match=match):
        secrets.padLeft("101010101110", 1025)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_node_py_padLeft_spotCheck():
    py_command = secrets.getRNG()
    py_random = py_command(11)
    assert len(secrets.padLeft(py_random, 0)) == 11
    assert len(secrets.padLeft(py_random, 1)) == 11
    assert len(secrets.padLeft(py_random, 3)) == 12
    assert len(secrets.padLeft(py_random, 5)) == 15
    assert len(secrets.padLeft(py_random, 7)) == 14
    assert len(secrets.padLeft(py_random, 8)) == 16
    assert len(secrets.padLeft(py_random, 9)) == 18
    assert len(secrets.padLeft(py_random, 10)) == 20


def test_node_py_padLeft(prime_numbers, multiple_numbers):
    secrets.init()
    py_command = secrets.getRNG()
    py_random = py_command(prime_numbers)
    py_string = secrets.padLeft(py_random, multiple_numbers)
    js_string = node._padLeft(py_random, multiple_numbers)
    assert py_string == js_string
    assert len(py_string) == len(js_string)
    assert (len(py_string) % multiple_numbers) == 0
    assert (len(js_string) % multiple_numbers) == 0


def random_range(input_range):
    block_size = int(65536 / (input_range + 1))
    # bits = (block_size * (input_range + 1)) - random.randrange(0, block_size)
    bits = (1 + block_size) - random.randrange(0, block_size)
    return bits


# @pytest.mark.parametrize("input_range", range(random.randrange(2, 128)))
@pytest.mark.parametrize("input_range", range(300))
def test_py_js_random(input_range):
    # bits = random_range(input_range)
    bits = int(input_range * 188) + 2
    secrets.init()
    secrets.setRNG("testRandom")
    py_string = secrets.random(bits)
    js_string = node.random(bits, test=True)
    assert py_string == js_string


@pytest.mark.parametrize("input_range", range(300))
def test_py_js_hex2bin(input_range):
    # bits = random_range(input_range)
    bits = int(input_range * 188) + 2
    secrets.init()
    secrets.setRNG()
    hex_string = secrets.random(bits)
    py_string = secrets.hex2bin(hex_string)
    js_string = node._hex2bin(hex_string)
    assert py_string == js_string


def test_hex2bin_Fail():
    match = "Invalid hex character:"
    with pytest.raises(ValueError, match=match):
        secrets.hex2bin("0123efgh")
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


@pytest.fixture(params=[None, 128, 256, 384, 512, 640, 768, 896, 1024])
def multiple_of_bits(request):
    return request.param


# Define your test function
def test_array_split(random_string, multiple_of_bits):
    hex_string = secrets.str2hex(random_string)
    bin_string = "1" + secrets.hex2bin(hex_string)

    py_array = secrets.splitNumStringToIntArray(bin_string, multiple_of_bits)
    js_array = node._splitNumStringToIntArray(bin_string, multiple_of_bits)

    # Iterate over the elements of one array
    for i in range(len(py_array)):
        assert py_array[i] == js_array[i]


@pytest.fixture(
    params=[None, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
)
def set_init_bits(request):
    return request.param


# Define test cases
@pytest.mark.parametrize(
    "x, coeffs",
    [
        (1, [21, 47, 205]),
        (2, [21, 47, 205]),
        (3, [21, 47, 205]),
        (4, [21, 47, 205]),
        (5, [21, 47, 205]),
        (6, [21, 47, 205]),
        (1, [0, 215, 162, 173, 194, 32, 53]),
        (2, [0, 215, 162, 173, 194, 32, 53]),
        (3, [0, 215, 162, 173, 194, 32, 53]),
        (4, [0, 215, 162, 173, 194, 32, 53]),
        (5, [0, 215, 162, 173, 194, 32, 53]),
        (6, [0, 215, 162, 173, 194, 32, 53]),
        (7, [0, 215, 162, 173, 194, 32, 53]),
        (8, [0, 215, 162, 173, 194, 32, 53]),
        (9, [0, 215, 162, 173, 194, 32, 53]),
        (10, [0, 215, 162, 173, 194, 32, 53]),
        (11, [0, 215, 162, 173, 194, 32, 53]),
        (12, [0, 215, 162, 173, 194, 32, 53]),
        (13, [0, 215, 162, 173, 194, 32, 53]),
        (14, [0, 215, 162, 173, 194, 32, 53]),
        (15, [0, 215, 162, 173, 194, 32, 53]),
        (16, [0, 215, 162, 173, 194, 32, 53]),
        (17, [0, 215, 162, 173, 194, 32, 53]),
        (18, [0, 215, 162, 173, 194, 32, 53]),
        (19, [0, 215, 162, 173, 194, 32, 53]),
        (20, [0, 215, 162, 173, 194, 32, 53]),
        (21, [0, 215, 162, 173, 194, 32, 53]),
        # Add more test cases as needed
    ],
)
def test_horner(x, coeffs, set_init_bits):
    secrets.init(set_init_bits)
    # assert secrets.horner(x, coeffs) == node._horner(x, coeffs)

    node_data = []
    node_data.append(node.init(set_init_bits, list=True))
    node_data.append(node._horner(x, coeffs, list=True))
    js_results = chain(node_data)

    assert secrets.horner(x, coeffs) == js_results[-1]


def test_getShares(set_init_bits):
    secrets.init(set_init_bits, "testRandom")
    py_results = secrets.getShares(1234, 6, 3)

    node_data = []
    node_data.append(node.init(set_init_bits, "testRandom", list=True))
    node_data.append(node._getShares(1234, 6, 3, list=True))
    js_results = chain(node_data)

    for i in range(6):
        assert py_results[i]["x"] == js_results[-1][i]["x"]
        assert py_results[i]["y"] == js_results[-1][i]["y"]
    assert True


def test_random_dithering():
    random_list = []

    def dithering(random_string):
        random_list.append(hex(int(random_string)))

    # Check dithering disabled
    secrets.init()
    secrets.getShares(1234, 6, 3)
    assert len(set(random_list)) == 0

    # Enable dithering
    settings.update_defaults(dithering=lambda string: dithering(string))
    secrets.getShares(1234, 6, 3)
    # print(random_list)
    assert len(set(random_list)) > 1

    # Check testRandom values are the same
    random_list = []
    secrets.init(8, "testRandom")
    settings.update_defaults(dithering=lambda string: dithering(string))
    secrets.getShares(1234, 6, 3)
    assert len(set(random_list)) == 1

    # Check dithering disabled
    random_list = []
    secrets.init()
    secrets.getShares(1234, 6, 3)
    assert len(set(random_list)) == 0


@pytest.fixture(
    params=[
        None,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    ]
)
def full_range_of_bits(request):
    return request.param


# Select a number of random shares
def pieces(shares, number=3):
    random.shuffle(shares)  # Randomize
    return shares[-number:]


def test_py_share(full_range_of_bits):
    # Generate shares with python
    secrets.init(full_range_of_bits)
    secret = secrets.random(128)

    # A few cold runs to cover non-zero in rng
    secrets.share(secret, 7, 6)
    secrets.share(secret, 7, 6)
    secrets.share(secret, 7, 6)

    shares = secrets.share(secret, 6, 3)

    # Combine shares using the JavaScript
    result = node.combine(pieces(shares, 3))
    assert result == secret


def test_py_share_error_string():
    match = "Secret must be a hex string."
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secrets.share(12345, 6, 3)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_py_share_error_shares():
    match = "Number of shares must be an integer"
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 1, 1)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, "hello", 3)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_py_share_error_high_shares():
    match = "Number of shares must be"
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 800, 3)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_py_share_error_threshold():
    match = "Threshold number of shares must be an integer >= 2."
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, 1)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, "two")
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_py_share_error_high_threshold():
    match = "Threshold number of shares must be"
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, 800)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, 7)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_py_share_error_padding():
    match = "Zero-pad length must be an integer between 0 and 1024 inclusive."
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, 3, "hello")
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, 3, -1)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        secrets.share(secret, 6, 3, 1025)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_py_random_error():
    match = "Number of bits must be an Integer between 2 and 65536."
    with pytest.raises(ValueError, match=match):
        secret = secrets.random(65538)
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_extractShareComponents_py(full_range_of_bits):
    # Generate shares with python
    secrets.init(full_range_of_bits)
    secret = secrets.random(128)
    shares = secrets.share(secret, 6, 3)
    shuffle = pieces(shares)

    py_result = secrets.extractShareComponents(shuffle[0])
    js_result = node.extractShareComponents(shuffle[0])
    assert py_result["bits"] == js_result["bits"]
    assert py_result["id"] == js_result["id"]
    assert py_result["data"] == js_result["data"]


def test_extractShareComponents_js(full_range_of_bits):
    secret = secrets.random(128)
    # Generate shares with node
    node_data = []
    node_data.append(node.init(full_range_of_bits, list=True))
    node_data.append(node.share(secret, 6, 3, list=True))
    js_results = chain(node_data)

    shuffle = pieces(js_results[-1])

    py_result = secrets.extractShareComponents(shuffle[0])
    js_result = node.extractShareComponents(shuffle[0])
    assert py_result["bits"] == js_result["bits"]
    assert py_result["id"] == js_result["id"]
    assert py_result["data"] == js_result["data"]


def test_lagrange_simple():
    secrets.init()
    js_poly = node._lagrange(
        0, [1, 2, 3, 4, 5, 6], [79, 123, 68, 175, 144, 164]
    )
    polynomial = secrets.lagrange(
        0, [1, 2, 3, 4, 5, 6], [79, 123, 68, 175, 144, 164]
    )
    assert polynomial == js_poly
    polynomial = secrets.lagrange(0, [1, 2, 3, 4, 5], [79, 123, 68, 175, 144])
    assert polynomial == js_poly
    polynomial = secrets.lagrange(0, [1, 2, 3, 4], [79, 123, 68, 175])
    assert polynomial == js_poly
    polynomial = secrets.lagrange(0, [1, 2, 3], [79, 123, 68])
    assert polynomial == js_poly
    polynomial = secrets.lagrange(0, [1, 2], [79, 123])
    assert polynomial != js_poly
    polynomial = secrets.lagrange(0, [1], [79])
    assert polynomial != js_poly


def test_combine_js2py(full_range_of_bits):
    secrets.init(full_range_of_bits)
    secret = secrets.random(128)
    # Generate shares with node
    node_data = []
    node_data.append(node.init(full_range_of_bits, list=True))
    node_data.append(node.share(secret, 6, 3, list=True))
    js_results = chain(node_data)

    shuffle = pieces(js_results[-1])
    # print(shuffle)

    py_result = secrets.combine(shuffle)
    assert py_result == secret


def test_combine_py2py(full_range_of_bits):
    secrets.init(full_range_of_bits)
    secret = secrets.random(128)
    # Generate shares with node
    shares = secrets.share(secret, 6, 3)

    shuffle = pieces(shares)
    # print(shuffle)

    py_result = secrets.combine(shuffle)
    assert py_result == secret


def test_new_shares(full_range_of_bits):
    secrets.init(full_range_of_bits)
    secret = secrets.random(128)
    shares = secrets.share(secret, 6, 3)

    result = secrets.newShare(7, shares)

    chunks = pieces(shares, 2)
    chunks.append(result)

    py_result = secrets.combine(chunks)
    assert py_result == secret


def test_rng_trigger_non_zero():
    secrets.init(3)
    secret = secrets.random(128)
    for i in range(256):
        shares = secrets.share(secret, 7, 5, 1024)
        assert len(shares) == 7


def test_combine_mismatch():
    match = "Mismatched shares: Different bit settings."
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        eight_bit = secrets.share(secret, 6, 3)

        secrets.init(10)
        ten_bit = secrets.share(secret, 6, 3)

        shuffle_eight = pieces(eight_bit)
        shuffle_ten = pieces(ten_bit)

        secrets.combine(eight_bit)
        secrets.combine(ten_bit)

        secrets.combine([shuffle_eight[0], shuffle_ten[1], shuffle_eight[2]])
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_combine_invalid():
    match = "Invalid share data provided."
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        shares = secrets.share(secret, 6, 3)

        shuffle = pieces(shares)

        secrets.combine([shares[0], "hello world", shares[2]])
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)


def test_new_share_invalid():
    match = "Invalid share data provided."
    with pytest.raises(ValueError, match=match):
        secrets.init()
        secret = secrets.random(32)
        shares = secrets.share(secret, 6, 3)

        shuffle = pieces(shares)

        secrets.newShare(277, shuffle[0])
        # Check if any warnings were raised
        assert len(caught_warnings) == 1
        assert issubclass(caught_warnings[0].category, Warning)
        assert match in str(caught_warnings[0].message)
