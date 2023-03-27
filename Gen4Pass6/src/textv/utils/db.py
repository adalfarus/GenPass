from utils.crypt import aes_encrypt
from utils.crypt import aes_decrypt
from rich.console import Console
console = Console()
import sqlite3
import os
    
def database_config(db_file, config):
    h_mp = config['default_mp']
    salt = config['default_salt']
    keys = list(config.keys())
    values = list(config.values())
    db = connect_to_database(db_file)
    c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS secrets (masterkey_hash TEXT NOT NULL, salt TEXT NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS passwords (ID INTEGER PRIMARY KEY AUTOINCREMENT, ACCOUNT TEXT NOT NULL, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL, IV_ACCOUNT BLOB NOT NULL, IV_USERNAME BLOB NOT NULL, IV_PASSWORD BLOB NOT NULL, TAG_ACCOUNT BLOB NOT NULL, TAG_USERNAME BLOB NOT NULL, TAG_PASSWORD BLOB NOT NULL)')
    c.execute('CREATE TABLE IF NOT EXISTS settings (setting_id TEXT PRIMARY KEY, setting_value TEXT NOT NULL)')
    c.execute('INSERT INTO secrets (masterkey_hash, salt) values (?, ?)', (h_mp, salt))
    for key, value in zip(keys, values):
        c.execute('INSERT INTO settings (setting_id, setting_value) values (?, ?)', (key, value))
    db.commit()
    db.close()
    
def database_update_secrets(database_file, hashed_mp, salt):
    db = connect_to_database(database_file)
    cursor = db.cursor()
    cursor.execute('UPDATE secrets SET MASTERKEY_HASH=?, SALT=?', (hashed_mp, salt))
    db.commit()
    db.close()
    
def database_update_passwords(database_file, account, username, password, password_id):
    db = connect_to_database(database_file)
    cursor = db.cursor()
    cursor.execute('UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=?, WHERE ID=?', (account, username, password, password_id))
    
def database_update_settings(database_file, setting_id, setting_value):
    db = connect_to_database(database_file)
    cursor = db.cursor()
    cursor.execute('UPDATE settings SET SETTINGS_VALUE=?, WHERE SETTING_ID=?', (setting_value, setting_id))

def connect_to_database(database_file):
    try:
        db = sqlite3.connect(database_file)
    except Exception as e:
        print("SQLite3 Error:", e)
        console.print_exception(show_locals=True)
    return db
    
def encrypt_all_data(database_file, key):
    x = '1'
    try:
        with connect_to_database(database_file) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute('SELECT * FROM passwords')
            rows = cursor.fetchall()
            for row in rows:
                id = row['ID']
                account = row['ACCOUNT']
                username = row['USERNAME']
                password = row['PASSWORD']
                iv_account, encrypted_account, tag_account = aes_encrypt(account, key)
                iv_username, encrypted_username, tag_username = aes_encrypt(username, key)
                iv_password, encrypted_password, tag_password = aes_encrypt(password, key)
                cursor.execute('UPDATE passwords SET ACCOUNT = ?, USERNAME = ?, PASSWORD = ?, IV_ACCOUNT = ?, IV_USERNAME = ?, IV_PASSWORD = ?, TAG_ACCOUNT = ?, TAG_USERNAME = ?, TAG_PASSWORD = ? WHERE ID = ?', (encrypted_account, encrypted_username, encrypted_password, iv_account, iv_username, iv_password, tag_account, tag_username, tag_password, id))
            db.commit()
    except Exception as e:
        print("SQLite3 Error:", e)
        console.print_exception(show_locals=True)
        x = 'a'
    return x.isnumeric()

def decrypt_all_data(database_file, key):
    x = 'a'
    try:
        with connect_to_database(database_file) as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute('SELECT * FROM passwords')
            rows = cursor.fetchall()
            for row in rows:
                id = row['ID']
                encrypted_account = row['ACCOUNT']
                encrypted_username = row['USERNAME']
                encrypted_password = row['PASSWORD']
                iv_account = row['IV_ACCOUNT']
                iv_username = row['IV_USERNAME']
                iv_password = row['IV_PASSWORD']
                tag_account = row['TAG_ACCOUNT']
                tag_username = row['TAG_USERNAME']
                tag_password = row['TAG_PASSWORD']
                decrypted_account = aes_decrypt(iv_account, encrypted_account, tag_account, key)
                decrypted_username = aes_decrypt(iv_username, encrypted_username, tag_username, key)
                decrypted_password = aes_decrypt(iv_password, encrypted_password, tag_password, key)
                cursor.execute('UPDATE passwords SET ACCOUNT = ?, USERNAME = ?, PASSWORD = ? WHERE ID = ?', (decrypted_account, decrypted_username, decrypted_password, id))
            db.commit()
    except Exception as e:
        print("SQLite3 Error:", e)
        console.print_exception(show_locals=True)
        x = '1'
    return x.isnumeric()
    
def is_database_encrypted(database_file):
    try:
        db = connect_to_database(database_file)
        cursor = db.cursor()
        cursor.execute('SELECT COUNT(*) FROM sqlite_master')
        cursor.close()
        db.close()
        return False
    except sqlite3.DatabaseError:
        return True
    
def is_data_encrypted(database_file):
    try:
        db = connect_to_database(database_file)
        cursor = db.cursor()
        cursor.execute('SELECT ACCOUNT FROM passwords LIMIT 1')
        account = cursor.fetchone()
        cursor.close()
        db.close()

        if account:
            # Check if the data appears to be encrypted (e.g., contains non-printable characters)
            return not all(char in string.printable for char in account[0])
        else:
            # The table is empty, so it's unclear if the data is encrypted or not
            return False
    except sqlite3.DatabaseError:
        return False
    
def check_database_simple(database_file):
    if os.path.exists(database_file):
        try:
            db = connect_to_database(database_file)
            db.close()
            return True
        except sqlite3.Error:
            return False
    else:
        return False
    
def check_database_simple_out(database_file):
    if os.path.exists(database_file):
        try:
            db = connect_to_database(database_file)
            db.close()
            print("Database", database_file, "exists.")
        except sqlite3.Error:
            print("SQLite3 Error: Unable to connect to database", database_file,".")
    else:
        print("Database", database_file, "does not exist.")
    return ""
    
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
    except Exception as e:
        print("SQLite3 Error:", e)
        console.print_exception(show_locals=True)
    return ""
    
def check_database_complex_output(database_file):
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
        except Exception as e:
            print("SQLite3 Error:", e)
    else:
        print("Database", database_file, "does not exist.")
