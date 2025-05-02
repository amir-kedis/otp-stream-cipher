import secrets
from venv import logger
from src.auth import HMACAuthenticator, encrypt_and_authenticate
from src.communication import CommunicationHandler
from src.key_exchange import DiffieHellman
from src.lcg import LCG
from src.seed_crypto import SeedEncryption
from src.stream_cipher import StreamCipher


class OneTimePadSystem:
    def __init__(self, config: dict):
        self.config = config
        self.comm = CommunicationHandler(
            host=config["network"]["host"], port=config["network"]["port"]
        )
        self.dh = DiffieHellman(
            p=config["diffie_hellman"]["p"], g=config["diffie_hellman"]["g"]
        )

    def int_to_bytes(self, n: int) -> bytes:
        return n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")

    def bytes_to_int(self, b: bytes) -> int:
        return int.from_bytes(b, byteorder="big")

    def generate_seed(self) -> int:
        return secrets.randbits(256)

    def sender(self, input_file: str):
        try:
            # Start server
            self.comm.start_server()
            self.comm.accept_connection()

            # Key exchange
            logger.info("Starting key exchange...")
            public_key = self.dh.get_public_value()
            public_key = self.int_to_bytes(public_key)
            self.comm.send_data(public_key)
            peer_public_key = self.comm.receive_data()
            peer_public_key = self.bytes_to_int(peer_public_key)
            print(peer_public_key)
            shared_key = self.dh.compute_shared_secret(peer_public_key)
            logger.info("Key exchange completed")

            # Initialize encryption and authentication
            seed_encryptor = SeedEncryption(shared_key)
            authenticator = HMACAuthenticator(shared_key)

            # Generate and encrypt seed
            logger.info("Generating and encrypting seed...")
            seed = self.generate_seed()
            iv, encrypted_seed, mac = encrypt_and_authenticate(
                seed, seed_encryptor, authenticator
            )
            logger.info("Seed generated and encrypted")

            # Send encrypted seed and MAC
            logger.info("Sending encrypted seed and MAC...")
            self.comm.send_data((iv, encrypted_seed, mac))

            # Initialize stream cipher
            logger.info("Initializing stream cipher...")
            lcg = LCG(
                seed=seed,
                a=self.config["lcg"]["multiplier"],
                c=self.config["lcg"]["increment"],
                m=self.config["lcg"]["modulus"],
            )
            cipher = StreamCipher(lcg)

            # Read and encrypt file
            with open(input_file, "rb") as f:
                logger.info(f"Reading file: {input_file}")
                plaintext = f.read()

            # Process in chunks of 10 characters
            chunk_size = 10
            for i in range(0, len(plaintext), chunk_size):
                logger.debug(f"Processing chunk: {i // chunk_size + 1}")
                chunk = plaintext[i : i + chunk_size]
                encrypted_chunk = cipher.encrypt(chunk)
                self.comm.send_data(encrypted_chunk)

            # Send end of transmission signal
            logger.info("Sending end of transmission signal...")
            self.comm.send_data(None)
            logger.info("Transmission completed")

        finally:
            self.comm.close()

    def receiver(self, output_file: str):
        """Implement receiver logic"""
        try:
            # Connect to server
            self.comm.start_client()

            # Key exchange
            logger.info("Starting key exchange...")
            peer_public_key = self.comm.receive_data()
            peer_public_key = self.bytes_to_int(peer_public_key)
            public_key = self.dh.get_public_value()
            public_key = self.int_to_bytes(public_key)
            self.comm.send_data(public_key)
            shared_key = self.dh.compute_shared_secret(peer_public_key)

            # Initialize encryption and authentication
            seed_encryptor = SeedEncryption(shared_key)
            authenticator = HMACAuthenticator(shared_key)

            # Receive and verify encrypted seed
            iv, encrypted_seed, mac = self.comm.receive_data()
            message = iv + encrypted_seed
            if not authenticator.verify_hmac(message, mac):
                raise ValueError("HMAC verification failed!")

            # Decrypt seed
            seed = seed_encryptor.decrypt(iv, encrypted_seed)

            # Initialize stream cipher
            lcg = LCG(
                seed=seed,
                a=self.config["lcg"]["multiplier"],
                c=self.config["lcg"]["increment"],
                m=self.config["lcg"]["modulus"],
            )
            cipher = StreamCipher(lcg)

            # Receive and decrypt data
            with open(output_file, "wb") as f:
                while True:
                    encrypted_chunk = self.comm.receive_data()
                    if encrypted_chunk is None:  # End of transmission
                        break
                    decrypted_chunk = cipher.decrypt(encrypted_chunk)
                    f.write(decrypted_chunk)

            logger.info("Reception and decryption completed")

        finally:
            self.comm.close()
