from rich.console import Console
from rich import print
console = Console()
error_console = Console(stderr=True, style="bold red")
import sys
import os

def error(location, reason, notes):
    error_console.print(location, "Error:", reason, "\nNotes:", notes, sep=' ')

def check_db_and_create(config):
    if config['mode'] == 'default':
        db_file = resource_path("passwords.db")
        if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
            print("Missing passwords.db, creating a new one...")
            db_config(db_file, config)
            check_db_complex_out(db_file)
    elif config['mode'] == 'esd':
        db_file1 = resource_path("passwords.db")
        secrets = ""
        db_file2 = secrets
        if not os.path.exists(db_file1) or os.path.getsize(db_file1) == 0:
            print("Missing passwords.db, creating a new one...")
            db_config(db_file1, config)
            check_db_complex_out(db_file1)
        if not os.path.exists(db_file2) or os.path.getsize(db_file2) == 0:
            print("Missing secrets.db, trying to create a new one at the closest location to the original...")
            try:
                db_config(db_file2, config)
                check_db_complex_out(db_file2)
            except Exception as e:
                print("SQLite3 Error:", e)
                console.print_exception(show_locals=True)
    elif config['mode'] == 'special':
        # Custom Order Mode for extra Security
        print("Requires Custom Order")
    else:
        print("Corrupted Config Tupel, please replace Database or contact creator")
    return None

error("Startup", "Error Test", "All ok, no action needed")