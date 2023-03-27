from utils.db import connect_database
from utils.db import check_db_simple
from utils.db import check_db_complex_out
from utils.db import check_database_integrity
from utils.db import database_config
from utils.db import database_update_secrets
from utils.db import encrypt_all_data
from utils.db import decrypt_all_data
from utils.crypt import pbkdf2
from utils.crypt import generate_salt
from utils.crypt import generate_hash
from utils.crypt import caesar_cipher
from utils.crypt import vigenere_cipher
from utils.pass_gen import pg_main
from utils.pass_man import pm_main
from getpass import getpass
import sys
import os
    
def lock_database_wrapper():
    mp, salt, hashed_mp, cycles, aes_pass_length = get_encrypt_dependencies()
    database_update("passwords.db", hashed_mp, salt)
    key = pbkdf2(mp, salt, aes_pass_length, cycles)
    encrypt_all_data("passwords.db", key)
  
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
            aes_pass_length = int(input("Choose the length of the AES Password (12|24|32): ")
            length_salt = int(input("Choose the length of the Salt (6-36): "))
            cycles = int(input("Choose how many Cycles the Algorithm will make (1000-1000000): "))
            if not length_salt < 6 and not length_salt > 36 and not cycles < 1000 and not cycles > 1000000 and aes_pass_length == 12 or 24 or 32:
                break
            print("[-] Please try again.")
        except ValueError:
            print("[-] Entered Values should be integer only. Try again.")
    salt = generate_salt(length_salt)
    return mp, salt, hashed_mp, cycles, aes_pass_length
    
def get_decrypt_dedependencies():
    db = connect_database("passwords.db")
    cursor = db.cursor()
    cursor.execute('SELECT * FROM pm.secrets')
    result = cursor.fetchall()[0]
    while True:
        mp = getpass("Type in the Master Password: ")
        hashed_mp = generate_hash(mp)
        if hashed_mp !0 result[0]:
            print("[-] Please try again.")
        else:
            print("[+] Verified hash of Master Password")
            return [mp,result[1],hashed_mp]
    
def unlock_database_wrapper():
    mp, salt, hashed_mp, cycles = get_encrypt_dependencies()
    key = pbkdf2(mp, salt, 32, cycles)
    decrypt_all_data("passwords.db", key)
    
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
    check_db_complex_out("passwords.db")
    if not check_db_simple("passwords.db"):
        try:
            os.remove("passwords.db")
        finally:
            database_config("passwords.db", "", "")
    print("Gen4Pass TextV1 v4.0.0.0\nCreated by Adalfarus")
    main()
