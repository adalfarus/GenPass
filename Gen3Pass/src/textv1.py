#from utils.db import check
#from utils.db import check_database
#from utils.db import check_database_integrity
#from utils.db import is_database_locked
#from utils.db import create_database
##from utils.db import encrypt_all_data
##from utils.db import decrypt_all_data
##from utils.db import make_key
#from utils.pass_gen import pg_main
#from utils.crypt import generate_hash
#from utils.crypt import caesar_cipher
#from utils.crypt import vigenere_cipher
#from utils.pass_man import pm_main
from getpass import getpass
import random
import string
import sqlite3
import sys
import os

def main():
    while True:
        action = input("0:Password Generation\n1:Password Manager\n2:Crypt\n3:Settings\n4:Exit\n->")
        if action == '0':
            action = input("0: Choose own Characters\n1: Choose Character Types\n2: With a sentence\n->")
            if action == '0':
                password_length = int(input("Length: "))
                extra_char = input("Type in your extra Character/s, spaces are counted as Character/s too: ")
                letters, digits, specialchar, deduct_symbols = '', '', ''
                print(generate_password(password_length, deduct_symbols, letters, digits, specialchar, extra_char))
            elif action == '1':
                password_length = int(input("Length: "))
                action_list = input("Enter character types you want to use, separate with dots ((A)Alphabet.(D)Digits.(SC)Special Characters.(ALL)All): ").split(".")
                letters = string.ascii_letters if "A" in action_list else ''
                digits = string.digits if "D" in action_list else ''
                special_char = string.punctuation if "SC" in action_list else ''
                if "ALL" in action_list:
                    letters, digits, specialchar = string.ascii_letters, string.digits, string.punctuation
                extra_char = input("Type in your extra Character/s, spaces are counted as Character/s too: ")
                deduct_symbols = input("Deduct Symbol(s): ")
                print(generate_password(password_length, deduct_symbols, letters, digits, special_char, extra_char))
            elif action == '2':
                words = input("Sentence: ").split(' ')
                char_position, random_case, extra_char, num_length, special_chars_length = 'random', False, '', 0, 0
                word_chars = [(word[min(char_position, len(word) - 1)] if char_position != 'random' else random.choice(word)) for word in words]
                if random_case:
                    word_chars = [char.lower() if random.random() < 0.5 else char.upper() for char in word_chars]
                num_string = ''.join(random.choices(string.digits, k=num_length))
                special_chars_string = ''.join(random.choices(string.punctuation, k=special_chars_length))
                print(''.join(word_chars) + extra_char + num_string + special_chars_string)
            else:
                print("Invalid choice. Please try again.")
        elif action == '1':
            while True:
                action = input("1:Add New Password\n2:View Saved Passwords\n3:Update Existing Password\n4:Delete Password\n5:Back\n->")
                if action == "1":
                    account = input("Enter account name: ")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                elif action == "2":
                    view_passwords()
                elif action == "3":
                    update_password()
                elif action == "4":
                    delete_password()
                elif action == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif action == '2':
            pass
        elif action == '3':
            pass
        else:
            print("Invalid choice. Please try again.")
    main()

    IV_ACCOUNT, IV_USERNAME, IV_PASSWORD = 0, 0, 0
    conn.execute("INSERT INTO passwords (ACCOUNT, USERNAME, PASSWORD, IV_ACCOUNT, IV_USERNAME, IV_PASSWORD) VALUES (?, ?, ?, ?, ?, ?)", (account, username, password, IV_ACCOUNT, IV_USERNAME, IV_PASSWORD))
    conn.commit()
    print("Password added successfully!")

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.abspath("."), filename)

import sqlite3
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from os import urandom

# Create a connection to the database
conn = sqlite3.connect('passwords.db')

# Create the table if it doesn't exist
conn.execute('''CREATE TABLE IF NOT EXISTS passwords
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ACCOUNT BLOB NOT NULL,
             USERNAME BLOB NOT NULL,
             PASSWORD BLOB NOT NULL);''')

def encrypt_data(key, data):
    chacha = ChaCha20Poly1305(key)
    nonce = urandom(12)
    ciphertext = chacha.encrypt(nonce, data, None)
    return nonce + ciphertext

def decrypt_data(key, data):
    chacha = ChaCha20Poly1305(key)
    nonce, ciphertext = data[:12], data[12:]
    plaintext = chacha.decrypt(nonce, ciphertext, None)
    return plaintext

def encrypt_all_data(key):
    cursor = conn.execute("SELECT ID, ACCOUNT, USERNAME, PASSWORD FROM passwords")
    for row in cursor:
        encrypted_account = encrypt_data(key, row[1])
        encrypted_username = encrypt_data(key, row[2])
        encrypted_password = encrypt_data(key, row[3])

        conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", (encrypted_account, encrypted_username, encrypted_password, row[0]))
        conn.commit()

def decrypt_all_data(key):
    cursor = conn.execute("SELECT ID, ACCOUNT, USERNAME, PASSWORD FROM passwords")
    for row in cursor:
        decrypted_account = decrypt_data(key, row[1])
        decrypted_username = decrypt_data(key, row[2])
        decrypted_password = decrypt_data(key, row[3])

        conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", (decrypted_account, decrypted_username, decrypted_password, row[0]))
        conn.commit()

# Replace this with your actual 256-bit key
key = urandom(32)

# Encrypt all data in the database
encrypt_all_data(key)

# Decrypt all data in the database
decrypt_all_data(key)

# Close the connection to the database
conn.close()

def generate_password(length, deduct_symbols, letters, digits, special_char, extra_char):
    characters = set(letters + digits + special_char + specharacters)
    deduct_symbols_set = set(deduct_symbols)
    filtered_characters = list(characters  - deduct_symbols_set)
    if not filtered_characters:
        print("Error: Filtered characters list is empty. Please adjust your inputs.")
        return None
    password_length = min(length, len(filtered_characters))
    password = ''.join(random.choice(filtered_characters) for _ in range(length))
    return password

main()