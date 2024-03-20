import secrets

def generate_non_zero_bits(bits):
    while True:
        result = bin(secrets.randbits(bits))[2:].zfill(bits)
        if '1' in result:
            return result

# Example usage:
bits = 8  # Number of bits required
random_bits = generate_non_zero_bits(bits)
print("Random bits:", random_bits)
