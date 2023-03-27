from utils.db import check_database
from utils.db import check_database_integrity
from utils.db import is_database_locked
from utils.db import create_encrypted_database
from utils.db import encrypt_database
from utils.db import decrypt_database
from utils.pass_gen import pg_main
from utils.crypt import generate_hash
from utils.crypt import caesar_cipher
from utils.crypt import vigenere_cipher
from utils.pass_man import pm_main
from getpass import getpass
import sys
import os

def get_master_password():
    master_password = getpass("Please input the Master Password: ")
    return master_password
    
def lock_database_wrapper():
    master_password = get_master_password()
    encrypt_database("passwords.db", master_password)
    
def unlock_database_wrapper():
    master_password = get_master_password()
    decrypt_database("passwords.db", master_password)
    
def use_limet_wrapper():
    print("Gen4Pass TextV1 can only use Limet, because it was designed for ultra low power applications.")
    
def check_database_integrity_wrapper():
    check_database_integrity("passwords.db")
    
def pass_gen_wrapper():
    pg_main()
    main()
    
def pass_man_wrapper():
    pm_main()
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
    print("Gen4Pass TextV1 can't use AES, because it was designed for ultra low power applications.")
    
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
    
def main():
    options = {
        "0": pass_gen_wrapper,
        "1": pass_man_wrapper,
        "2": crypt_wrapper,
        "3": settings,
        "4": sys.exit
    }
    while True:
        action = input("0:Password Generation\n1:Password Manager\n2:Crypt\n3:Settings\n4:Exit\n->")
        if action in options:
            options[action]()
            break
        else:
            print("Invalid choice. Please try again.")
    main()
    
if __name__ == "__main__":
    check_database("passwords.db")
    if not check():
        try:
            os.remove("passwords.db")
        finally:
            create_encrypted_database("passwords.db", get_master_password())
    print("Gen4Pass TextV1 v4.0.0.0\nCreated by Adalfarus")
    main()
