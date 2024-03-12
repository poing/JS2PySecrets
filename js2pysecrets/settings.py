# settings.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class Defaults:
    bits: int = 8  # default number of bits
    radix: int = 16  # work with HEX by default
    min_bits: int = 3
    max_bits: int = 20  # This allows up to 1,048,575 shares
    bytes_per_char: int = 2
    max_bytes_per_char: int = 6  # Math.pow(256,7) > Math.pow(2,53)

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


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.defaults = Defaults()
            cls._instance.current_settings = Defaults()
        return cls._instance

    def get_defaults(self):
        return self.defaults

    def update_defaults(self, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self.defaults, key):
                    setattr(self.defaults, key, value)
        else:
            self.defaults = Defaults()  # Reset to default values

    def reset_defaults(self):
        self.defaults = Defaults()
