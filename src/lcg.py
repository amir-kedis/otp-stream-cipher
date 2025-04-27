"""LCG: Linear Congruential Generator."""


class LCG:
    """Linear Congruential Generator (LCG) for pseudo-random number generation."""

    def __init__(self, a: int, c: int, m: int, seed: int):
        self.a = a
        self.c = c
        self.m = m
        self.current = seed

    def next(self) -> int:
        """Generate the next pseudo-random number."""
        self.current = (self.a * self.current + self.c) % self.m
        return self.current

    def generate_keystream(self, length: int) -> bytes:
        """Generate a keystream of the specified length."""
        return bytes(self.next() & 0xFF for _ in range(length))
