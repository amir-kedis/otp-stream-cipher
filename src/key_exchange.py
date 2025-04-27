"""Using Diffie-Hellman key exchange"""

import logging

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh

logger = logging.getLogger(__name__)


class DiffieHellman:
    def __init__(self, p: str, g: int):
        """
        Initialize DH with parameters from config
        p: Prime number in hexadecimal string format
        g: Generator value
        """
        # Convert hex string to integer
        self.P = int(p, 16)
        self.G = g

        try:
            # Create parameter numbers
            self.parameters = dh.DHParameterNumbers(self.P, self.G)
            # Convert to parameters object
            self.param_object = self.parameters.parameters(default_backend())
            # Generate private key
            self.private_key = self.param_object.generate_private_key()
            self.public_key = self.private_key.public_key()
        except Exception as e:
            logger.error(f"Error initializing DH parameters: {e}")
            raise ValueError(f"Invalid DH parameters: {e}")

    def get_public_value(self) -> int:
        """Get public value to send to other party"""
        # Convert public key to numbers
        pub_numbers = self.public_key.public_numbers()
        return pub_numbers.y

    def compute_shared_secret(self, other_public_value: int) -> bytes:
        """Compute shared secret from other party's public value"""
        try:
            # Create public key object from other party's value
            peer_pub_numbers = dh.DHPublicNumbers(other_public_value, self.parameters)
            peer_public_key = peer_pub_numbers.public_key(default_backend())

            # Compute shared secret
            shared_key = self.private_key.exchange(peer_public_key)
            return shared_key

        except Exception as e:
            logger.error(f"Error in key exchange: {e}")
            raise ValueError(f"Error computing shared key: {e}")
