import sqlite3

# create connection to the database
conn = sqlite3.connect('passwords.db')

# create table if it doesn't exist
conn.execute('''CREATE TABLE IF NOT EXISTS passwords
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ACCOUNT TEXT NOT NULL,
             USERNAME TEXT NOT NULL,
             PASSWORD TEXT NOT NULL,
             IV_ACCOUNT BLOB NOT NULL,
             IV_USERNAME BLOB NOT NULL,
             IV_PASSWORD BLOB NOT NULL);''')

# function to add new password to the database
def add_password():
    account = input("Enter account name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    IV_ACCOUNT, IV_USERNAME, IV_PASSWORD = 0, 0, 0
    conn.execute("INSERT INTO passwords (ACCOUNT, USERNAME, PASSWORD, IV_ACCOUNT, IV_USERNAME, IV_PASSWORD) VALUES (?, ?, ?, ?, ?, ?)", (account, username, password, IV_ACCOUNT, IV_USERNAME, IV_PASSWORD))
    conn.commit()
    print("Password added successfully!")

# function to view all saved passwords
def view_passwords():
    cursor = conn.execute("SELECT * from passwords")
    print("{:<5} {:<15} {:<15} {:<15}".format("ID", "Account", "Username", "Password"))
    print("="*50)
    for row in cursor:
        print("{:<5} {:<15} {:<15} {:<15}".format(row[0], row[1], row[2], row[3]))
    print("="*50)

# function to update existing password
def update_password():
    password_id = input("Enter password ID to update: ")
    account = input("Enter new account name: ")
    username = input("Enter new username: ")
    password = input("Enter new password: ")
    conn.execute("UPDATE passwords SET ACCOUNT=?, USERNAME=?, PASSWORD=? WHERE ID=?", (account, username, password, password_id))
    conn.commit()
    print("Password updated successfully!")

# function to delete password
def delete_password():
    password_id = input("Enter password ID to delete: ")
    conn.execute("DELETE from passwords WHERE ID=?", (password_id,))
    conn.commit()
    print("Password deleted successfully!")

# main function to run the password manager program
def pm_main():
    while True:
        choice = input("1:Add New Password\n2:View Saved Passwords\n3:Update Existing Password\n4:Delete Password\n5:Back\n->")
        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            update_password()
        elif choice == "4":
            delete_password()
        elif choice == "5":
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    pm_main()
