import os
import sqlite3
import pysqlitecipher

from pysqlcipher3 import dbapi2 as sqlcipher

def create_encrypted_database(database_file, password):
    try:
        conn = sqlcipher.connect(database_file)
        conn.execute("PRAGMA key='{}'".format(password))
        conn.execute("PRAGMA cipher_compatibility = 4")
        conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
        conn.close()
        print("Encrypted database created successfully.")
    except sqlite3.Error as e:
        print("SQLite3 Error: ", e)

def query_encrypted_database(database_file, password, query):
    try:
        conn = sqlcipher.connect(database_file)
        conn.execute("PRAGMA key='{}'".format(password))
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print("SQLite3 Error: ", e)

def encrypt_database(database_path, key):
    conn = sqlcipher.connect(database_path)
    conn.execute(f"PRAGMA key='{key}'")
    conn.execute("PRAGMA cipher_compatibility = 4")
    conn.execute("PRAGMA cipher_use_hmac = OFF")
    conn.execute("PRAGMA cipher_page_size = 4096")
    conn.execute("PRAGMA kdf_iter = 64000")
    conn.execute("PRAGMA cipher_default_kdf_algorithm = ARGON2")
    conn.execute("SELECT count(*) FROM sqlite_master;")
    cursor = conn.cursor()
    for row in cursor:
        count = row[0]
    cursor.close()
    conn.close()
    
def decrypt_database(database_path, key):
    conn = sqlcipher.connect(database_path)
    conn.execute(f"PRAGMA key='{key}'")
    conn.execute("PRAGMA cipher_compatibility = 4")
    conn.execute("PRAGMA cipher_use_hmac = OFF")
    conn.execute("PRAGMA cipher_page_size = 4096")
    conn.execute("PRAGMA kdf_iter = 64000")
    conn.execute("PRAGMA cipher_default_kdf_algorithm = ARGON2")
    conn.execute("SELECT count(*) FROM sqlite_master;")
    cursor = conn.cursor()
    for row in cursor:
        count = row[0]
    cursor.close()
    conn.close()
    
#    try:
#        if result[0] == "ok":
#            print("Database", database_file, "is not corrupted.")
#        else:
#            print("Database", database_file, "is corrupted.")
#    except sqlite3.Error as e:
#        print("SQLite3 Error:", e)

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

def check(database_file):
    if os.path.exists(database_file):
        try:
            conn = sqlite3.connect(database_file)
            conn.close()
            return True
        except sqlite3.Error:
            return False
    else:
        return False
        
#def check(database_file):
#    if os.path.exists(database_file):
#        try:
#            conn = sqlite3.connect(database_file)
#            conn.close()
#            print("Database", database_file, "exists.")
#        except sqlite3.Error:
#            print("SQLite3 Error: Unable to connect to database", database_file,".")
#    else:
#        print("Database", database_file, "does not exist.")

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
        print("SQLite3 Error:", e)

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
            print("SQLite3 Error:", e)
    else:
        print("Database", database_file, "does not exist.")
