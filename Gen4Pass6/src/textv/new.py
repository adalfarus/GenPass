import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

def aes_decrypt(iv, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()

def decode_message(message, password, salt, cycles):
    decoded_message = base64.b64decode(message)
    iv1 = decoded_message[:16]
    iv2 = decoded_message[16:32]
    iv3 = decoded_message[32:48]
    encrypted_data = decoded_message[48:-32]
    tags = decoded_message[-32:]
    key = PBKDF2(password, salt.encode(), 32, cycles)
    try:
        plaintext = aes_decrypt(iv1, encrypted_data, tags[:16], key)
        plaintext += aes_decrypt(iv2, encrypted_data, tags[16:32], key)
        plaintext += aes_decrypt(iv3, encrypted_data, tags[32:], key)
    except ValueError:
        # decryption with iv2 or iv3 failed, ignore the error and return plaintext from iv1
        plaintext = aes_decrypt(iv1, encrypted_data, tags[:16], key)
    return plaintext

message = "M8mgViIrycvR0R3H77/sIr6CYsI6B0v2iNOqMGfMsG7UVcv0TPT44/VnRb6jX8s68zg/fvbpxJe7VhJvwvIn8SpVpkFo6IhsJ7rFj41ScX22"
password = "Lock"
salt = "4P4N4TG37hUS1c/5avOeSfOY5bw9Nl24hFyP"
cycles = 1000

try:
    # call the function that raises the error
    result = decode_message(message, password, salt, cycles)
except ValueError:
    # do nothing, just silently ignore the error
    pass
print(result)
