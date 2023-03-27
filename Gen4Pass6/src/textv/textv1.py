from utils.db import connect_to_database as connect_db
from utils.db import check_database_simple as check_db_simple
from utils.db import check_database_complex_output as check_db_complex_out
from utils.db import check_database_integrity as check_db_corrupt
from utils.db import database_config as db_config
from utils.db import database_update_secrets as db_update
from utils.db import encrypt_all_data
from utils.db import decrypt_all_data
from utils.crypt import pbkdf2
from utils.crypt import generate_salt
from utils.crypt import generate_hash
from utils.crypt import caesar_cipher
from utils.crypt import vigenere_cipher
from utils.pass_gen import pg_main
from utils.pass_man import add_password
from utils.pass_man import view_passwords
from utils.pass_man import update_password
from utils.pass_man import delete_password
from getpass import getpass
import sys
import os

connect_to_database as connect_db, check_database_simple as check_db_simple,
                      check_database_complex_output as check_db_complex_out, check_database_integrity as check_db_corrupt,
                      database_config as db_config, database_update_secrets as db_update,
                      encrypt_all_data, decrypt_all_data
    
default_setting_ids = ['theme', 
                       'cryptlib', 
                       'encrypted', 
                       'uselimet', 
                       'default_mp', 
                       'default_salt', 
                       'auto_locking']

default_setting_val = ['system|dark|light', 
                       'esdm|caeser|default', 
                       'true|false', 
                       'false|true', 
                       'Master Password', 
                       'SaltSaltSaltSalt'
                       'true']
    
def pass_gen_wrapper():
    pg_main()
    main()
    
def pass_man_wrapper():
    db = connect_db('passwords.db')
    while True:
        action = input("1. Add New Password\n2. View Saved Passwords\n3. Update Existing Password\n4. Delete Password\n5. Back\n->")
        if action == "1":
            add_password(db)
        elif action == "2":
            view_passwords(db)
        elif action == "3":
            update_password(db)
        elif action == "4":
            delete_password(db)
        elif action == "5":
            db.close()
            break
        else:
            print("Invalid choice. Please try again.")
    main()
    
def crypt_wrapper():
    options = {
        "0": aes_wrapper,
        "1": hash_wrapper,
        "2": ccipher_wrapper,
        "3": vcipher_wrapper,
        "4": main
    }
    
    while True:
        action = input("0:AES\n1:Hash\n2:Caeser cipher\n3:Vigenère cipher\n4:Back\n->")
        if action in options:
            options[action]()
            break
        else:
            print("Invalid choice. Please try again.")
    crypt_wrapper()
    
def aes_wrapper():
    print("Gen4Pass TextV1 can't use AES, because it was designed for ultra low power applications. If you want to use it however, please get Gen4Pass TextV2 instead.")
    
def hash_wrapper():
    hashed_input = generate_hash(input("Text to be Hashed: "))
    print("Hashed Text:", hashed_input)
    
def ccipher_wrapper():
    cintext = input("Text to be cciphered: ").lower()
    cshift = int(input("Shift Value: "))
    couttext = caesar_cipher(cintext, cshift)
    print("CCiphered text:", couttext)
    
def vcipher_wrapper():
    vintext = input("Text to be vciphered: ").upper()
    vkeyword = input("Keyword: ").upper()
    vencrypt = input("Encrypt: ")
    vouttext = vigenere_cipher(vintext, vkeyword, vencrypt)
    print("VCiphered text:", vouttext)
    
def settings():
    options = {
        "0": lock_database_wrapper,
        "1": unlock_database_wrapper,
        "2": use_limet_wrapper,
        "3": check_database_integrity_wrapper,
        "4": main
    }
    
    while True:
        action = input("0:Lock Database\n1:Unlock Database\n2:Uselimet\n3:Check Database Integrity\n4:Back\n->")
        if action in options:
            options[action]()
            break
        else:
            print("Invalid choice. Please try again.")
    settings()
    
def lock_database_wrapper():
    mp, hashed_mp, salt, aes_pass_length, cycles = get_encrypt_dependencies()
    db_update(resource_path("passwords.db"), hashed_mp, salt)
    key = pbkdf2(mp, salt, aes_pass_length, cycles)
    encrypt_all_data(resource_path("passwords.db"), key)
    
def get_encrypt_dependencies():
    while True:
        mp = getpass("Choose a Master Password: ")
        if mp == getpass("Re-type: ") and mp != "":
            break
        print("[-] Please try again.")
    hashed_mp = generate_hash(mp)
    print("[+] Generated hash of Master Password")
    while True:
        try:
            aes_pass_length = int(input("Choose the length of the AES Password (16|24|32): "))
            length_salt = int(input("Choose the length of the Salt (6-36): "))
            cycles = int(input("Choose how many Cycles the Algorithm will make (1000-1000000): "))
            if not length_salt < 6 and not length_salt > 36 and not cycles < 1000 and not cycles > 1000000 and aes_pass_length in (16, 24, 32):
                break
            print("[-] Please try again.")
        except ValueError:
            print("[-] Entered Values should be integer only. Try again.")
    salt = generate_salt(length_salt)
    return mp, hashed_mp, salt, aes_pass_length, cycles
    
def unlock_database_wrapper():
    mp, hashed_mp, salt, aes_pass_length, cycles = get_decrypt_dependencies()
    key = pbkdf2(mp, salt, aes_pass_length, cycles)
    decrypt_all_data(resource_path("passwords.db"), key)
    
def get_decrypt_dependencies():
    db = connect_db(resource_path("passwords.db"))
    cursor = db.cursor()
    cursor.execute('SELECT * FROM secrets')
    result = cursor.fetchall()[0]
    while True:
        mp = getpass("Type in the Master Password: ")
        hashed_mp = generate_hash(mp)
        if hashed_mp != result[0]:
            print("[-] Please try again.")
        else:
            print("[+] Verified hash of Master Password")
            break
    aes_pass_length = int(input("Please input the length of the AES Password: "))
    cycles = int(input("Please input how many Cycles the Algorithm ran for: "))
    if not cycles < 1000 and not cycles > 1000000 and aes_pass_length in (16, 24, 32):
        return [mp, hashed_mp, result[1], aes_pass_length, cycles]
    
def use_limet_wrapper():
    print("Gen4Pass TextV1 can only use Limet, because it was designed for ultra low power applications. If you don't want to use it however, please get Gen4Pass TextV2 instead.")
    
def check_database_integrity_wrapper():
    check_db_corrupt(resource_path("passwords.db"))
    
def info():
    print("Gen4Pass TextV1 \n-Was developed for ultra low power applications\n-Is very secure, when locked (Every Possible Password Combination * 3 000 000)")
    
def main():
    options = {
        "0": pass_gen_wrapper,
        "1": pass_man_wrapper,
        "2": crypt_wrapper,
        "3": settings,
        "4": info,
        "5": sys.exit
    }
    while True:
        action = input("0:Password Generation\n1:Password Manager\n2:Crypt\n3:Settings\n4:Info\n5:Exit\n->")
        if action in options:
            options[action]()
            break
        else:
            print("Invalid choice. Please try again.")
    main()

def resource_path(filename):
    """Return the absolute path to a file in the app's resource directory."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, filename)
    else:
        # In development mode, use the absolute path to the file
        return os.path.join(os.path.abspath("."), filename)
    
if __name__ == "__main__":
    if not os.path.exists(resource_path("passwords.db")) or os.path.getsize(resource_path("passwords.db")) == 0:
        db_config(resource_path("passwords.db"), "", "")
    check_db_complex_out(resource_path("passwords.db"))
    print("Gen4Pass TextV1 v4.0.0.0\nCreated by Adalfarus")
    main()
