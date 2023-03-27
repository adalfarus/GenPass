from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
    
# The key must be 16, 24, or 32 bytes long, and the IV must be 12 bytes long
def make_key(password, salt, cycles):
	key = PBKDF2(password.encode(), salt.encode(), 32, count=cycles, hmac_hash_module=SHA512).encode()
    return key
    
def encrypt(data, key):
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return iv, ciphertext, tag

def decrypt(iv, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except ValueError:
        print("MAC check failed")
        return None
    
def generate_hash(message):
    sha256 = SHA256.new(data=message.encode())
    return sha256.hexdigest()
    
def caesar_cipher(intext, shift):
    outtext = ""
    for i in range(len(intext)):
        temp = ord(intext[i]) + shift
        if temp > 122:
            temp_diff = temp - 122
            temp = 96 + temp_diff
        elif temp < 97:
            temp_diff = 97 - temp
            temp = 123 - temp_diff
        outtext += chr(temp)
    return outtext

def vigenere_cipher(text, keyword, encrypt=True):
    key = list(keyword)
    if len(text) == len(key):
        key = key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    key = "".join(key)
    if encrypt=="True":
        outtext = []
        for i in range(len(text)):
            x = (ord(text[i]) + ord(key[i])) % 26
            x += ord('A')
            outtext.append(chr(x))
        outtext = "".join(outtext)
    elif encrypt=="False":
        outtext = []
        for i in range(len(text)):
            x = (ord(text[i]) - ord(key[i]) + 26) % 26
            x += ord('A')
            outtext.append(chr(x))
        outtext = "".join(outtext)
    else:
        outtext = ""
        print("Encrypt can only be True or False")
    return outtext