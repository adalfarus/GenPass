import sqlite3

from rich import print as printc
from rich.console import Console
console = Console()

def dbconfig():
    try:
        db = sqlite3.connect('database.db') # Connect to the SQLite database
    except Exception as e:
        console.print_exception(show_locals=True)


    return db
