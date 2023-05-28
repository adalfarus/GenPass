from utils import (CryptUtils, Database, GeneratePasswords, PasswordManager)
from getpass import getpass
from rich.console import Console
from rich import print
console = Console()
error_console = Console(stderr=True, style="bold red")
import sys
import os

db = Database()

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.abspath("."), filename)

def check_db_and_create(config):
    if config['mode'] == 'default':
        db_file = resource_path("passwords.db")
        if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
            print("Missing passwords.db, creating a new one...")
            db.database_config(db_file, config)
            db.check_database_complex_output(db_file)
    elif config['mode'] == 'esd':
        db_file1 = resource_path("passwords.db")
        secrets = ""
        db_file2 = secrets
        if not os.path.exists(db_file1) or os.path.getsize(db_file1) == 0:
            print("Missing passwords.db, creating a new one...")
            db.database_config(db_file1, config)
            db.check_database_complex_output(db_file1)
        if not os.path.exists(db_file2) or os.path.getsize(db_file2) == 0:
            print("Missing secrets.db, trying to create a new one at the closest location to the original...")
            try:
                db.database_config(db_file2, config)
                db.check_database_complex_output(db_file2)
            except Exception as e:
                print("SQLite3 Error:", e)
                console.print_exception(show_locals=True)
    elif config['mode'] == 'special':
        # Custom Order Mode for extra Security
        print("Requires Custom Order")
    else:
        print("Corrupted Config Tupel, please replace Database or contact creator")
    return None

def pass_gen_wrapper():
    main()

def pass_man_wrapper():
    main()

def back_pm_wrapper(db):
    db.close()
    main()

def crypt_wrapper():
    main()

def settings():
    main()

def main():
    input()
    main()

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
