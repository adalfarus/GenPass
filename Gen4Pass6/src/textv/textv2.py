from utils.dbv2 import (check_db_and_create)
from utils.crypt import (pbkdf2, generate_salt, generate_hash, caesar_cipher, vigenere_cipher)
from utils.pass_gen import pg_main
from utils.pass_man import (add_password, view_passwords, update_password, delete_password)
from getpass import getpass
from rich.console import Console
from rich import print
console = Console()
error_console = Console(stderr=True, style="bold red")
import sys
import os

def pass_gen_wrapper():
    main()

def pass_man_wrapper():
    db = connect_db(resource_path("passwords.db"))
    options = {
        "0": add_password,
        "1": view_passwords,
        "2": update_password,
        "3": delete_password,
        "4": back_pm_wrapper}
    while True:
        action = input("0. Add New Password\n1. View Saved Passwords\n2. Update Existing Password\n3. Delete Password\n4. Back\n->")
        if action in options:
            options[action](db)
            break
        else:
            print("Invalid choice. Please try again.")
    pass_man_wrapper()

def back_pm_wrapper(db):
    db.close()
    main()

def crypt_wrapper():
    options = {
        "0": aes_wrapper,
        "1": hash_wrapper,
        "2": ccipher_wrapper,
        "3": vcipher_wrapper,
        "4": main}
    while True:
        action = input("0:AES\n1:Hash\n2:Caeser cipher\n3:Vigenere cipher\n4:Back\n->")
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
        "4": main}
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
    print("Infos: Version, ...")
    main()

def main():
    options = {
        "0": pass_gen_wrapper,
        "1": pass_man_wrapper,
        "2": crypt_wrapper,
        "3": settings,
        "4": info,
        "5": sys.exit}
    while True:
        action = input("0:Password Generation\n1:Password Manager\n2:Crypt\n3:Settings\n4:Info\n5:Exit\n->")
        if action in options:
            options[action]()
            break
        else:
            print("Invalid choice. Please try again.")
    main()

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.abspath("."), filename)

if __name__ == "__main__":
    configuration = {
        'theme': 'system',
        'mode': 'default',
        'encrypted': 'false',
        'uselimet': 'false',
        'default_mp': 'Master Password',
        'default_salt': 'SaltSaltSaltSalt',
        'auto_locking': 'true',
        'debug': 'false'}
    try:
        check_db_and_create(configuration)
    except Exception as e:
        print("DatabaseError: ", e)
    finally:
        print("[bold black]█████▀████████████████████████████████████████████")
        print("[bold black]█─▄▄▄▄█▄─▄▄─█▄─▀█▄─▄█░█░██▄─▄▄─██▀▄─██─▄▄▄▄█─▄▄▄▄█")
        print("[bold red]█─██▄─██─▄█▀██─█▄▀─██▄▄░███─▄▄▄██─▀─██▄▄▄▄─█▄▄▄▄─█")
        print("[bold yellow]▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▀▄▄▄▀▀▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀")
        print("[bold italic yellow on red blink]Gen4Pass6 TextV2 v.4.0.6.0 Created by Adalfarus")
        main()
