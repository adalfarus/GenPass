from utils.dbconfig import dbconfig
from getpass import getpass
from Crypto.Hash import SHA256
from Crypto.Random.random import *
import string
import os

from rich import print as printc
from rich.console import Console

console = Console()


def generateDeviceSecret(length):
    return ''.join(sample(string.ascii_lowercase + string.digits, k=length))


def config(): # Create a database
    db = dbconfig()
    cursor = db.cursor() # Create a cursor object
    
    # Create Tables
    query = "CREATE TABLE IF NOT EXISTS secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")

    query = "CREATE TABLE IF NOT EXISTS entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    query = "CREATE TABLE IF NOT EXISTS settings (settings TEXT NOT NULL)"
    res = cursor.execute(query)
    printc("[green][+][/green] Table 'settings' created")

    while True:
        mp = getpass("Choose a Master Password: ")
        if mp == getpass("Re-type: ") and mp != "":
            break
        printc("[yellow][-] Please try again.[/yellow]")

    # Hash the Master Password
    hashed_mp = SHA256.new(data=b'{mp}').hexdigest()
    printc("[green][+][/green] Generated hash of Master Password")

    while True:
        try:
            length = int(input("Choose the length of the Device Secret (6-36): "))
            if not length<6 and not length>36:
                break
            printc("[yellow][-] Please try again.[/yellow]")
        except ValueError:
            print("Entered Value should be an integer only. Try again.")
    
    # Generate the Device Secret
    ds = generateDeviceSecret(length)
    printc("[green][+][/green] Device Secret generated")

    # Add them to db
    query = "INSERT INTO secrets (masterkey_hash, device_secret) values (?, ?)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added to database")

    printc("[green][+] Configuration done![/green]")

    db.close()


if __name__ == '__main__':
    try:
        os.remove("database.db")
    except Exception as e:
        print('Failed: '+ str(e))
    finally:
        config()
