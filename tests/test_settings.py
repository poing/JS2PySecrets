import js2pysecrets.base as secrets
import js2pysecrets.node as node
import pytest
from js2pysecrets.settings import Settings

settings = Settings()


def test_defaults():
    settings.reset_defaults()
    defaults = settings.get_defaults()
    assert callable(defaults.rng) == True
    assert defaults.bits == 8
    assert defaults.radix == 16
    assert defaults.min_bits == 3
    assert defaults.max_bits == 20
    assert defaults.bytes_per_char == 2
    assert defaults.max_bytes_per_char == 6


def test_update_defaults():
    settings.update_defaults(bits=16)
    settings.update_defaults(max_bits=16)
    defaults = settings.get_defaults()
    assert defaults.bits == 16
    assert defaults.max_bits == 16
    assert defaults.bits == defaults.max_bits


def test_update_reset():
    settings.update_defaults(bits=16)
    settings.update_defaults(max_bits=16)
    defaults = settings.get_defaults()
    assert defaults.bits == 16
    assert defaults.max_bits == 16
    settings.update_defaults()
    defaults = settings.get_defaults()
    assert defaults.bits == 8
    assert defaults.max_bits == 20


def test_reset_defaults():
    settings.update_defaults(bits=16)
    settings.update_defaults(max_bits=16)
    defaults = settings.get_defaults()
    assert defaults.bits == 16
    assert defaults.max_bits == 16
    settings.reset_defaults()
    defaults = settings.get_defaults()
    assert defaults.bits == 8
    assert defaults.max_bits == 20


def test_get_config():
    config = settings.get_config()
    assert config.bits == 8
    assert config.radix == 16
    assert config.maxShares == 255
    assert config.hasCSPRNG == False
    assert config.typeCSPRNG == None


def test_get_updated_config():
    settings.update_defaults(bits=2)
    settings.update_defaults(radix=4)
    # settings.update_defaults(rng="hello world")
    settings.update_defaults(maxShares=6)
    settings.update_defaults(hasCSPRNG=True)
    settings.update_defaults(typeCSPRNG="hello world")
    config = settings.get_config()
    assert config.bits == 2
    assert config.radix == 4
    # assert callable(settings.rng) == False
    assert config.maxShares == 6
    assert config.hasCSPRNG == True
