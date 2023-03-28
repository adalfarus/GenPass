from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
data = "My Data"
nonce = get_random_bytes(12)
key = b'\xf8bG\xd6I\x95\xe1m\xfa+\xd8\xed"\xe6\x8bA\xd2\x97\x16a\x0c\x0b\xaf\x95\xf8\x18\xca\x10\x9a\x0e\x10\xe2'
chacha = ChaCha20_Poly1305.new(key=key)
ciphertext, tag = chacha.encrypt_and_digest(data, nonce)
print(ciphertext, tag)
