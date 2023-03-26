from Crypto.Hash import SHA256
    
def generate_hash(message):
    """
    Generates a SHA-256 hash of the given message
    :param message: The message to hash
    :return: The hashed message as a hexadecimal string
    """
    # Convert the message to bytes
    message_bytes = message.encode('utf-8')

    # Create a new SHA-256 hash object
    sha256 = SHA256.new()

    # Update the hash object with the message bytes
    sha256.update(message_bytes)

    # Return the hashed message as a hexadecimal string
    return sha256.hexdigest()
    
def caesar_cipher(intext, shift):
    """
    Applies a Caesar cipher to the given text using the specified shift value
    :param intext: The text to cipher
    :param shift: The number of positions to shift each character in the text
    :return: The ciphered text
    """
    outtext = ""
    for i in range(len(intext)):
        # Convert the current character to its ASCII code and add the shift value
        temp = ord(intext[i]) + shift
        
        # Wrap around to the beginning of the alphabet if necessary
        if temp > 122:
            temp_diff = temp - 122
            temp = 96 + temp_diff
        elif temp < 97:
            temp_diff = 97 - temp
            temp = 123 - temp_diff
        
        # Convert the new ASCII code back to a character and add it to the output text
        outtext += chr(temp)
    
    return outtext

def vigenere_cipher(text, keyword, encrypt=True):
    # Generate Key
    key = list(keyword)
    if len(text) == len(key):
        key = key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
    key = "".join(key)
    # Check encrypt Variable
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