from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes
from getpass import getpass
import random
import string
import base64
import sqlite3
import sys
import os

def main():
    while True:
        action = input("0:Password Generation\n1:Password Manager\n2:Crypt\n3:Settings & Info\n4:Exit\n->")
        if action == '0':
            while True:
                action = input("0: Choose own Characters\n1: Choose Character Types\n2: With a sentence\n3: Back\n->")
                if action == '0':
                    password_length = int(input("Length: "))
                    extra_char = input("Type in your extra Character/s, spaces are counted as Character/s too: ")
                    letters, digits, specialchar, deduct_symbols = '', '', '', ''
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
                elif action == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif action == '1':
            while True:
                action = input("1:Add New Password\n2:View Saved Passwords\n3:Update Existing Password\n4:Delete Password\n5:Back\n->")
                if action == '1':
                    account = input("Enter account name: ")
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    conn.execute("INSERT INTO passwords (ACCOUNT, USERNAME, PASSWORD) VALUES (?, ?, ?)", (account, username, password))
                    conn.commit()
                    print("Password added successfully!")
                elif action == '2':
                    cursor = conn.execute("SELECT * from passwords")
                    print("{:<5} {:<15} {:<15} {:<15}".format("ID", "Account", "Username", "Password"))
                    print("="*50)
                    for row in cursor:
                        print("{:<5} {:<15} {:<15} {:<15}".format(row[0], row[1], row[2], row[3]))
                    print("="*50)
                elif action == '3':
                    password_id = input("Enter password ID to update: ")
                    account = input("Enter new account name: ")
                    username = input("Enter new username: ")
                    password = input("Enter new password: ")
                    conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", (account, username, password, password_id))
                    conn.commit()
                    print("Password updated successfully!")
                elif action == '4':
                    password_id = input("Enter password ID to delete: ")
                    conn.execute("DELETE from passwords WHERE ID=?", (password_id,))
                    conn.commit()
                    print("Password deleted successfully!")
                elif action == '5':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif action == '2':
            while True:
                action = input("0: Caeser Cipher\n1: Vigerene Cipher\n2: Back\n->")
                if action == '0':
                    intext = ''.join(input("CCipher Text: ").split()).lower()
                    shift = int(input("Shift Value: "))
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
                    print("CCiphered Text: ", outtext)
                elif action == '1':
                    intext = input("VCipher Text: ")
                    keyword = input("Keyword: ")
                    encrypt = input("Encrypt: ").lower()
                    key = (keyword * ((len(intext) // len(keyword)) + 1))[:len(intext)]
                    outtext = ""
                    for i in range(len(intext)):
                        if intext[i].isalpha():
                            shift = ord(key[i])
                            if encrypt == "true":
                                x = (ord(intext[i]) + shift % 26)
                            elif encrypt == "false":
                                x = (ord(intext[i]) - shift % 26)
                            else:
                                print("Encrypt can only be True or False")
                                return
                            outtext += chr(x)
                        else:
                            outtext += intext[i]
                    print("VCiphered Text: ", outtext)
                elif action == '2':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif action == '3':
            while True:
                action = input("0: Always Clear Screen\n1: Info\n2: Back\n->")
                if action == '0':
                    if acs:
                        acs = False
                        print("ACS set to", acs)
                    else:
                        acs = True
                        print("ACS set to", acs)
                elif action == '1':
                    print("This is Gen3Pass TextV1, this version always auto locks the database and auto saves settings, so please exit with the exit option.")
                elif action == '2':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif action == '4':
            hashed_mp, salt, key = get_mp(base64.b64encode(get_random_bytes(32)).decode('utf-8'))
            encrypt_all_data(key)
            conn.execute(f"UPDATE secrets SET hashed_mp = '{hashed_mp}', salt = '{salt}'")
            conn.commit()
            conn.close()
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
    main()

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.abspath("."), filename)

def generate_password(length, deduct_symbols, letters, digits, special_char, extra_char):
    characters = set(letters + digits + special_char + extra_char)
    deduct_symbols_set = set(deduct_symbols)
    filtered_characters = list(characters  - deduct_symbols_set)
    if not filtered_characters:
        print("Error: Filtered characters list is empty. Please adjust your inputs.")
        return None
    password_length = min(length, len(filtered_characters))
    password = ''.join(random.choice(filtered_characters) for _ in range(length))
    return password

def get_mp(salt):
    while True:
        mp = getpass("Master Password: ")
        if mp == getpass("Re-enter: ") and mp != '':
            # salt = base64.b64encode(get_random_bytes(32)).decode('utf-8')
            break
    hashed_mp = SHA256.new(mp.encode('utf-8')).hexdigest()
    key = HKDF(mp.encode(), 32, salt.encode(), SHA256)
    return hashed_mp, salt, key

def encrypt_data(key, data):
    chacha = ChaCha20_Poly1305.new(key=key)
    nonce = chacha.nonce  # Use the generated nonce from the cipher object
    ciphertext, tag = chacha.encrypt_and_digest(data.encode())
    return nonce + ciphertext + tag

def decrypt_data(key, data):
    nonce, ciphertext, tag = data[:12], data[12:-16], data[-16:]
    chacha = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    plaintext = chacha.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode()

def encrypt_all_data(key):
    cursor = conn.execute("SELECT ID, ACCOUNT, USERNAME, PASSWORD FROM passwords")
    for row in cursor:
        encrypted_account = encrypt_data(key, row[1])
        encrypted_username = encrypt_data(key, row[2])
        encrypted_password = encrypt_data(key, row[3])

        conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", 
                     (encrypted_account, encrypted_username, encrypted_password, row[0]))
        conn.commit()

def decrypt_all_data(key):
    cursor = conn.execute("SELECT ID, ACCOUNT, USERNAME, PASSWORD FROM passwords")
    for row in cursor:
        decrypted_account = decrypt_data(key, row[1])
        decrypted_username = decrypt_data(key, row[2])
        decrypted_password = decrypt_data(key, row[3])

        conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", 
                     (decrypted_account, decrypted_username, decrypted_password, row[0]))
        conn.commit()

def settings(db_element, id, value, update=False):
    if update:
        db_element.execute('UPDATE settings SET VALUE=? WHERE ID=?', (value, id))
        conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", (account, username, password, password_id))
    cursor.execute("SELECT id, value FROM settings")
    rows = cursor.fetchall()
    settings = {row[0]: row[1] for row in rows}
    acs = settings.get(1)
    return acs

if __name__ == "__main__":
    db_file = resource_path("passwords.db")
    try:
        if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
            conn = sqlite3.connect(db_file)
            conn.execute('''CREATE TABLE IF NOT EXISTS passwords
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            ACCOUNT BLOB NOT NULL,
                            USERNAME BLOB NOT NULL,
                            PASSWORD BLOB NOT NULL);''')
            conn.execute('''CREATE TABLE IF NOT EXISTS settings
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            VALUE BLOB NOT NULL);''')
            conn.execute('INSERT INTO settings (VALUE) VALUES (?)', ("False",))
            conn.execute('''CREATE TABLE IF NOT EXISTS secrets
                            (HASHED_MP NOT NULL,
                            SALT NOT NULL);''')
            conn.execute('INSERT INTO passwords (ACCOUNT, USERNAME, PASSWORD) VALUES (?, ?, ?)', ("Example", "Example", "Example"))
            conn.execute('INSERT INTO secrets (HASHED_MP, SALT) VALUES (?,?)', ('', ''))
            conn.commit()
            print("New Database created")
        else:
            print("Database Check complete")
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT hashed_mp, salt FROM secrets")
            hashed_mp, salt = cursor.fetchone()
            while True:
                mp, salt, key = get_mp(salt)
                if mp == hashed_mp:
                    decrypt_all_data(key)
                    break
                elif hashed_mp == '':
                    break
                else:
                    print("Invalid Key")
            conn.execute(f"UPDATE secrets SET hashed_mp = '{hashed_mp}', salt = '{salt}'")
    except Exception as e:
        print("Error: ", e)
    finally:

        print("█▀▀ █▀▀ █▄░█ █▀█ ▄▀█ █▀ █▀   ▀█▀ █▀▀ ▀▄▀ ▀█▀ █░█ ▄█")
        print("█▄█ ██▄ █░▀█ █▀▀ █▀█ ▄█ ▄█   ░█░ ██▄ █░█ ░█░ ▀▄▀ ░█")
        print("Gen3Pass TextV1 v.3.0.0.0 Created by Adalfarus\n")
        print("This is Gen3Pass TextV1, this version always auto locks the database and auto saves settings, so please exit with the exit option.")
        main()
