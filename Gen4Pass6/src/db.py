import os
import sqlite3
import os

from utils.crypt import encrypt
from utils.crypt import decrypt

def database_config(database, hashed_mp, salt):
    db = connect_database(database)
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS secrets (masterkey_hash TEXT NOT NULL, salt TEXT NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS passwords (ID INTEGER PRIMARY KEY AUTOINCREMENT, ACCOUNT TEXT NOT NULL, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL)')
    cursor.execute('INSERT INTO secrets (masterkey_hash, salt) values (?, ?)', (hashed_mp, salt))
    db.commit()
       
def connect_database(database):
    try:
        db = sqlite3.connect(database)
    except Exception as e:
        console.print_exception(show_locals=True)
    return db

def encrypt_all_data(database):
    with sqlite3.connect(database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM passwords')
        rows = c.fetchall()
        for row in rows:
            id = row['ID']
            account = row['ACCOUNT']
            username = row['USERNAME']
            password = row['PASSWORD']
            
            iv_account, encrypted_account, tag_account = encrypt(account, key)
            iv_username, encrypted_username, tag_username = encrypt(username, key)
            iv_password, encrypted_password, tag_password = encrypt(password, key)
            
            c.execute('UPDATE passwords SET ACCOUNT = ?, USERNAME = ?, PASSWORD = ?, IV_ACCOUNT = ?, IV_USERNAME = ?, IV_PASSWORD = ? WHERE ID = ?', (iv_account + encrypted_account + tag_account, iv_username + encrypted_username + tag_username, iv_password + encrypted_password + tag_password, iv_account, iv_username, iv_password, id))
        conn.commit()

def decrypt_all_data(database):
    with sqlite3.connect(database) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM passwords')
        rows = c.fetchall()
        for row in rows:
            id = row['ID']
            encrypted_account = row['ACCOUNT']
            encrypted_username = row['USERNAME']
            encrypted_password = row['PASSWORD']
            iv_account = row['IV_ACCOUNT']
            iv_username = row['IV_USERNAME']
            iv_password = row['IV_PASSWORD']
            tag_account = encrypted_account[-16:]
            tag_username = encrypted_username[-16:]
            tag_password = encrypted_password[-16:]
            decrypted_account = decrypt(iv_account, encrypted_account[12:-16], tag_account, key)
            decrypted_username = decrypt(iv_username, encrypted_username[12:-16], tag_username, key)
            decrypted_password = decrypt(iv_password, encrypted_password[12:-16], tag_password, key)
            c.execute('UPDATE passwords SET ACCOUNT = ?, USERNAME = ?, PASSWORD = ? WHERE ID = ?', (decrypted_account, decrypted_username, decrypted_password, id))
        conn.commit()

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
