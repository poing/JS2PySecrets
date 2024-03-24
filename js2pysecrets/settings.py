# settings.py
import secrets
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Defaults:
    rng = lambda self, bits: bin(secrets.randbits(bits))[2:].zfill(bits)
    dithering = None
    bits: int = 8  # default number of bits
    radix: int = 16  # work with HEX by default
    min_bits: int = 3
    max_bits: int = 20  # This allows up to 1,048,575 shares
    size: int = 0
    bytes_per_char: int = 2
    max_bytes_per_char: int = 6  # Math.pow(256,7) > Math.pow(2,53)
    maxShares: int = 255
    hasCSPRNG: bool = False
    typeCSPRNG: Optional[str] = None
    logs: List[None | int] = field(default_factory=lambda: [])
    exps: List[None | int] = field(default_factory=lambda: [])
    """
    Primitive polynomials (in decimal form) for Galois Fields GF(2^n),
    for 2 <= n <= 30  The index of each term in the array corresponds
    to the n for that polynomial i.e. to get the polynomial for n=16,
    use primitivePolynomials[16]
    """
    primitive_polynomials: List[None | int] = field(
        default_factory=lambda: [
            None,
            None,
            1,
            3,
            3,
            5,
            3,
            3,
            29,
            17,
            9,
            5,
            83,
            27,
            43,
            3,
            45,
            9,
            39,
            39,
            9,
            5,
            3,
            33,
            27,
            9,
            71,
            39,
            9,
            5,
            83,
        ]
    )


@dataclass
class Config:
    bits: int
    radix: int
    maxShares: int
    hasCSPRNG: bool
    typeCSPRNG: Optional[str]


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.defaults = Defaults()
            cls._instance.current_settings = Defaults()
        return cls._instance

    def __getattr__(self, attr):
        return getattr(self.defaults, attr)

    def get_defaults(self):
        return self.defaults

    @property
    def bits(self):
        return self.defaults.bits

    @property
    def radix(self):
        return self.defaults.radix

    @property
    def maxShares(self):
        return self.defaults.maxShares

    @property
    def hasCSPRNG(self):
        return self.defaults.hasCSPRNG

    @property
    def typeCSPRNG(self):
        return self.defaults.typeCSPRNG

    def get_config(self):
        return Config(
            radix=self.radix,
            bits=self.bits,
            maxShares=self.maxShares,
            hasCSPRNG=self.hasCSPRNG,
            typeCSPRNG=self.typeCSPRNG,
        )

    def update_defaults(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self.defaults, key):
                    setattr(self.defaults, key, value)
        else:
            self.defaults = Defaults()  # Reset to default values

    def reset_defaults(self):
        self.defaults = Defaults()
