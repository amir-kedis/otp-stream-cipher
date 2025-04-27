from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# 1. Generate some DH parameters (only once, can reuse later)
parameters = dh.generate_parameters(generator=2, key_size=2048)

# 2. Alice generates her private/public key
alice_private_key = parameters.generate_private_key()
alice_public_key = alice_private_key.public_key()

# 3. Bob generates his private/public key
bob_private_key = parameters.generate_private_key()
bob_public_key = bob_private_key.public_key()

# 4. Exchange public keys and compute the shared secret
# Alice computes shared key
alice_shared_key = alice_private_key.exchange(bob_public_key)

# Bob computes shared key
bob_shared_key = bob_private_key.exchange(alice_public_key)

# 5. Derive a symmetric key from the shared secret (recommended)
derived_key_alice = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"handshake data",
    backend=default_backend(),
).derive(alice_shared_key)

derived_key_bob = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"handshake data",
    backend=default_backend(),
).derive(bob_shared_key)

# 6. Now both have the same derived_key
print(derived_key_alice == derived_key_bob)  # Should print True
