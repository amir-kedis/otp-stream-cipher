"""Auth using HMAC"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac


class HMACAuthenticator:
    """HMAC Authenticator for signing and verifying messages."""

    def __init__(self, key: bytes):
        self.key = key

    def generate_hmac(self, message: bytes) -> bytes:
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=default_backend())
        h.update(message)
        return h.finalize()

    def verify_hmac(self, message: bytes, hmac_to_verify: bytes) -> bool:
        h = hmac.HMAC(self.key, hashes.SHA256(), backend=default_backend())
        h.update(message)

        try:
            # NOTE: throws if wrong
            h.verify(hmac_to_verify)
            return True
        except Exception:
            return False


def encrypt_and_authenticate(
    seed: int, seed_encryptor, hmac_authenticator: HMACAuthenticator
) -> tuple[bytes, bytes, bytes]:
    """Encrypt the seed and generate an HMAC for authentication."""
    iv, encrypted_seed = seed_encryptor.encrypt(seed)
    hmac_value = hmac_authenticator.generate_hmac(iv + encrypted_seed)
    return iv, encrypted_seed, hmac_value
