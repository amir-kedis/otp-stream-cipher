"""For Encrypting and Decrypting the seed I'm using AES."""

import logging
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logger = logging.getLogger(__name__)


class SeedEncryption:

    def __init__(self, key: bytes):
        hashed_key = hashes.Hash(hashes.SHA256(), backend=default_backend())
        hashed_key.update(key)
        self.key = hashed_key.finalize()

    def encrypt(self, seed: int) -> tuple[bytes, bytes]:

        seed_bytes = seed.to_bytes((seed.bit_length() + 7) // 8, byteorder="big")
        iv = os.urandom(16)

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(seed_bytes) + padder.finalize()

        logger.info(f"Key size: {len(self.key)}")
        logger.info(f"IV size: {len(iv)}")
        logger.info(f"key: {self.key}")

        cipher = Cipher(
            algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()
        )

        encryptor = cipher.encryptor()
        encrypted_seed = encryptor.update(padded_data) + encryptor.finalize()

        return iv, encrypted_seed

    def decrypt(self, iv: bytes, encrypted_seed: bytes) -> int:
        cipher = Cipher(
            algorithms.AES(self.key), modes.CBC(iv), backend=default_backend()
        )

        decryptor = cipher.decryptor()
        padded_seed = decryptor.update(encrypted_seed) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        seed_bytes = unpadder.update(padded_seed) + unpadder.finalize()

        return int.from_bytes(seed_bytes, byteorder="big")
