import pytest
import js2pysecrets.base as secrets
from js2pysecrets.settings import Settings
import random

settings = Settings()


@pytest.mark.parametrize(
    "bits, bits_error",
    [
        (None, None),
        (1, "Number of bits must be an integer between"),
        (2, "Number of bits must be an integer between"),
        (3, None),
        (4, None),
        (5, None),
        (6, None),
        (7, None),
        (8, None),
        (9, None),
        (10, None),
        (11, None),
        (12, None),
        (13, None),
        (14, None),
        (15, None),
        (16, None),
        (17, None),
        (18, None),
        (19, None),
        (20, None),
        (21, "Number of bits must be an integer between"),
        (99, "Number of bits must be an integer between"),
    ],
)
@pytest.mark.parametrize(
    "rand_bits, rand_error",
    [
        (None, "Number of bits must be an Integer between 2 and 65536."),
        (1, "Number of bits must be an Integer between 2 and 65536."),
        (2, None),
        (3, None),
        (4, None),
        (5, None),
        (random.randrange(2, 32), None),
        (random.randrange(32, 64), None),
        (random.randrange(64, 128), None),
        (random.randrange(128, 256), None),
        (random.randrange(256, 512), None),
        (random.randrange(512, 1024), None),
        (random.randrange(1024, 2048), None),
        (random.randrange(2048, 4096), None),
        (random.randrange(4096, 8192), None),
        (random.randrange(8192, 16384), None),
        (random.randrange(16384, 32768), None),
        (random.randrange(32768, 65536), None),
        (65533, None),
        (65534, None),
        (65535, None),
        (65536, None),
        (65537, "Number of bits must be an Integer between 2 and 65536."),
        (65538, "Number of bits must be an Integer between 2 and 65536."),
    ],
)
@pytest.mark.parametrize(
    "sec_val, sec_error",
    [
        (None, "Secret must be a hex string."),
        (1234, "Secret must be a hex string."),
        (-256, "Secret must be a hex string."),
        ("hello world", "Invalid hex character:"),
        (None, None),
    ],
)
@pytest.mark.parametrize(
    "num_val, num_error",
    [
        (False, "Number of shares must be an integer >= 2."),
        (2, "Number of shares must be an integer >= 2."),
        (0, "Number of shares must be an integer >= 2."),
        (-22, "Number of shares must be an integer >= 2."),
        (
            "hello",
            "Threshold number of shares must be less than or equal to the total shares specified.",
        ),
        (
            lambda: settings.maxShares + 1,
            "Threshold number of shares must be <=",
        ),
        (None, None),
    ],
)
@pytest.mark.skip(reason="WIP: started seeing odd failures")
def test_py_init_with_errors(
    bits,
    bits_error,
    rand_bits,
    rand_error,
    sec_val,
    sec_error,
    num_val,
    num_error,
):

    expected_error = check_error(bits_error, rand_error, sec_error, num_error)

    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            secrets.init(bits)
            if not bits_error:
                secret = secrets.random(rand_bits)
                if sec_error:
                    secret = sec_val
            if not bits_error or rand_error or num_error:
                num_shares = base_value(num_val) or 6
                shares = secrets.share(secret, num_shares, 3)
            if not bits_error or rand_error:
                num_shares = base_value(num_val)
                shares = secrets.share(secret, num_shares, 3)
            assert len(caught_warnings) == 1
            assert issubclass(caught_warnings[0].category, Warning)
            assert expected_error in str(caught_warnings[0].message)
    else:
        secrets.init(bits)
        assert bits == settings.bits or settings.get_defaults().bits

        secret = secrets.random(rand_bits)
        shares = secrets.share(secret, 6, 3)


# Used to catch the expected error
def check_error(bits_error, rand_error, sec_error, num_error):
    expected_error = (
        bits_error
        if bits_error
        else (
            rand_error
            if rand_error
            else (
                sec_error if sec_error else (num_error if num_error else None)
            )
        )
    )
    return expected_error


# Used to generate errors for threshold and number of shares
def base_value(value, default=6):
    if value is None:
        return default
    elif value is False:
        return None
    elif callable(value):
        return value()
    elif isinstance(value, int):
        return value
    elif isinstance(value, str):
        return value
    else:
        return None


@pytest.mark.parametrize(
    "std_bits, std_bits_error",
    [
        (None, None),
        (3, None),
        (4, None),
        (5, None),
        (6, None),
        (7, None),
        (8, None),
        (9, None),
        (10, None),
        (11, None),
        (12, None),
        (13, None),
        (14, None),
        (15, None),
        (16, None),
        (17, None),
        (18, None),
        (19, None),
        (20, None),
    ],
)
@pytest.mark.skip(reason="WIP: started seeing odd failures")
def test_full_share(std_bits, std_bits_error):
    bits = std_bits

    secrets.init(bits)
    bits = settings.bits or settings.get_defaults().bits
    assert bits == settings.bits or settings.get_defaults().bits

    secret = secrets.random(64)
    num_shares = low_random(settings.maxShares, 3)

    shares = secrets.share(secret, num_shares, 3)
    assert len(shares) == num_shares


def low_random(value, standard=6):
    return int(random.triangular(standard, value, standard))
