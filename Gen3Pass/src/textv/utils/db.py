import os
import sqlite3
import os

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64

def create_database():
    return ""

# Define the encryption key and initialization vector (IV)
# The key must be 16, 24, or 32 bytes long, and the IV must be 12 bytes long
def make_key(password, salt):
	key = PBKDF2(password.encode(), salt.encode(), 32, count=1000000, hmac_hash_module=SHA512).encode()
    key = b'{key}'

# 6-36
def generate_salt(length=36):
    return ''.join(sample(string.ascii_lowercase + string.digits, k=length))

def config():
    db = dbconfig()
    cursor = db.cursor() # Create a cursor object
    
    # Create Tables
    query = "CREATE TABLE IF NOT EXISTS secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    hashed_mp = SHA256.new(data=b'{mp}').hexdigest()
    
    # Add them to db
    query = "INSERT INTO secrets (masterkey_hash, device_secret) values (?, ?)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()
    
    
def dbconfig():
    try:
        db = sqlite3.connect('database.db') # Connect to the SQLite database
    except Exception as e:
        console.print_exception(show_locals=True)
    return db

def encrypt(data, key):
    iv = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return iv, ciphertext, tag

def decrypt(iv, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except ValueError:
        print("MAC check failed")
        return None

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
