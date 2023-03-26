#from pysqlcipher3 import dbapi2 as sqlcipher
import time
import os
import sqlite3

from rich import print as printc
from rich.console import Console

console = Console()

def create_encrypted_database(database_file, password):
    try:
        conn = sqlcipher.connect(database_file)
        conn.execute("PRAGMA key='{}'".format(password))
        conn.execute("PRAGMA cipher_compatibility = 4")
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
        conn.close()
        print("Encrypted database created successfully.")
    except sqlite3.Error as e:
        print("Error: ", e)

def query_encrypted_database(database_file, password):
    try:
        conn = sqlcipher.connect(database_file)
        conn.execute("PRAGMA key='{}'".format(password))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()
    except sqlite3.Error as e:
        print("Error: ", e)
        
def lock_encrypted_database(database_file, password):
    try:
        conn = sqlcipher.connect(database_file)
        conn.execute("PRAGMA key='{}'".format(password))
        conn.execute("PRAGMA cipher_default_use_hmac = OFF")
        conn.execute("PRAGMA cipher_page_size = 1024")
        conn.execute("PRAGMA cipher_hmac_algorithm = SHA1")
        conn.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1")
        conn.execute("PRAGMA cipher_use_kdf_iter = 64000")
        conn.execute("PRAGMA cipher_activate_extensions = 1")
        conn.execute("PRAGMA cipher_compatibility = 4")
        conn.execute("PRAGMA cipher_rekey = 'OFF'")
        conn.execute("PRAGMA cipher_plaintext_header_size = 0")
        conn.execute("PRAGMA rekey = NULL")
        conn.close()
        print("Encrypted database locked successfully.")
    except sqlite3.Error as e:
        print("Error: ", e)

def is_database_locked(database_file):
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute("PRAGMA query_only = true")
        cursor.execute("SELECT COUNT(*) FROM sqlite_master")
        cursor.close()
        conn.close()
        return False
    except sqlite3.DatabaseError:
        return True

def lock_database(database_file, password):
    try:
        conn = sqlite3.connect(database_file)
        conn.execute("PRAGMA key='{}'".format(password))
        conn.execute("PRAGMA cipher_default_use_hmac = OFF")
        conn.execute("PRAGMA cipher_page_size = 1024")
        conn.execute("PRAGMA cipher_hmac_algorithm = SHA1")
        conn.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA1")
        conn.execute("PRAGMA cipher_use_kdf_iter = 64000")
        conn.execute("PRAGMA cipher_activate_extensions = 1")
        conn.execute("PRAGMA cipher_compatibility = 4")
        conn.execute("PRAGMA cipher_rekey = 'OFF'")
        conn.execute("PRAGMA cipher_plaintext_header_size = 0")
        conn.execute("PRAGMA rekey = 'OFF'")
        conn.close()
        print("Database", database_file, "locked successfully.")
    except sqlite3.Error as e:
        print("Error: ", e)

def unlock_database(database_file, password):
    try:
        conn = sqlite3.connect(database_file)
        conn.execute("PRAGMA key='{password}'".format(password=password))
        conn.close()
        print("Database", database_file, "unlocked successfully.")
    except sqlite3.Error as e:
        print("Error: ", e)

def check(database_file):
    if os.path.exists(database_file):
        try:
            conn = sqlite3.connect(database_file)
            conn.close()
            print("Database", database_file, "exists.")
        except sqlite3.Error:
            print("Error: Unable to connect to database", database_file,".")
    else:
        print("Database", database_file, "does not exist.")
        time.sleep(3)


def check_database_integrity(database_file):
    try:
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()
        conn.close()

        if result[0] == "ok":
            print("Database", database_file, "is not corrupted.")
        else:
            print("Database", database_file, "is corrupted.")
    except sqlite3.Error as e:
        print("Error: ", e)

def check_database(database_file):
    if os.path.exists(database_file):
        try:
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()

            if result[0] == "ok":
                print("Database", database_file, "exists and is not corrupted.")
            else:
                print("Database", database_file, "exists but is corrupted.")
        except sqlite3.Error as e:
            print("Error: ", e)
    else:
        print("Database", database_file, "does not exist.")
