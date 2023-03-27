import sqlite3

def add_password(db):
    account = input("Enter account name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    placeholder_iv = b''
    placeholder_tag = b''
    db.execute("INSERT INTO passwords (ACCOUNT, USERNAME, PASSWORD, IV_ACCOUNT, IV_USERNAME, IV_PASSWORD, TAG_ACCOUNT, TAG_USERNAME, TAG_PASSWORD) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (account, username, password, placeholder_iv, placeholder_iv, placeholder_iv, placeholder_tag, placeholder_tag, placeholder_tag))
    db.commit()
    print("Password added successfully!")

    
def view_passwords(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM passwords")
    rows = cursor.fetchall()
    columns = ["ID", "Account", "Username", "Password"]
    decoded_rows = [[r.decode('raw_unicode_escape') if isinstance(r, bytes) else str(r) for r in row] for row in rows]
    width = [max(len(c), max(len(str(r[i])) for r in decoded_rows)) for i, c in enumerate(columns)]
    print("ID".ljust(width[0]), "Account".ljust(width[1]), "Username".ljust(width[2]), "Password".ljust(width[3]), sep="   ")
    print("=" * sum(width))# + 4))
    for row in decoded_rows:
        print(str(row[0]).ljust(width[0]), str(row[1]).ljust(width[1]), str(row[2]).ljust(width[2]), str(row[3]).ljust(width[3]), sep="   ")
    print("=" * sum(width))# + 4))
'''    print("=" * (width[0]-1), "|", "=" * (width[1]-1), "|", "=" * (width[2]-1), "|", "=" * width[3])'''
    
#def view_passwords(db):
#    cursor = db.cursor()
#    cursor.execute("SELECT * FROM passwords")
#    rows = cursor.fetchall()
#    columns = ["ID", "Account", "Username", "Password"]
#    width = [max(len(c), max(len(str(r[i])) for r in rows)) for i, c in enumerate(columns)]
#    print("ID".ljust(width[0]), "Account".ljust(width[1]), "Username".ljust(width[2]), "Password".ljust(width[3]), sep="|")
#    print("=" * (width[0]-1), "|", "=" * (width[1]-1), "|", "=" * (width[2]-1), "|", "=" * width[3])
#    for row in rows:
##        row = [str(r).encode('unicode_escape').decode() if isinstance(r, bytes) else str(r) for r in row]
#        row = ["³" + r.decode('unicode_escape') if isinstance(r, bytes) else str(r) for r in row]
#        print(str(row[0]).ljust(width[0]), str(row[1]).ljust(width[1]), str(row[2]).ljust(width[2]), str(row[3]).ljust(width[3]), sep="|")
#    print("=" * (width[0]-1), "|", "=" * (width[1]-1), "|", "=" * (width[2]-1), "|", "=" * width[3])

def update_password(db):
    password_id = input("Enter password ID to update: ")
    account = input("Enter new account name: ")
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    db.execute('UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?', (account, username, password, password_id))
    db.commit()
    print("Password updated successfully!")

def delete_password(db):
    password_id = input("Enter password ID to delete: ")
    db.execute('DELETE from passwords WHERE ID=?', (password_id,))
    db.commit()
    print("Password deleted successfully!")
