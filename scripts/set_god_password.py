import csv
import os
import sqlite3

import bcrypt

from src.db import build_db
from src.db.db import Db

dirname = os.path.dirname(__file__).replace("\\", "/")
cwd = os.getcwd().replace("\\", "/")
if dirname == cwd:
    os.chdir("..")

print("This script will set the God user and their password hash in the DB.")
print("")

try:
    db_obj = Db()
except FileNotFoundError:
    build_db.main()
    db_obj = Db()

with db_obj as db:
    if os.path.isfile("scripts/users.csv"):
        with open("scripts/users.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Role"] == "god":
                    db.set_god_user(
                        row["Username"],
                        row["Full Name"],
                        bcrypt.hashpw(row["Password"].encode(), bcrypt.gensalt())
                    )
                    print("God username and password have been saved to the DB.")
                else:
                    try:
                        db.add_user(
                            row["Username"],
                            row["Full Name"],
                            bcrypt.hashpw(row["Password"].encode(), bcrypt.gensalt()),
                            row["Role"]
                        )
                        print(f"Added '{row['Username']}' to the database.")
                    except sqlite3.IntegrityError as e:
                        if str(e) == "UNIQUE constraint failed: users.username":
                            print(f"'{row['Username']}' is already in the database. Skipping...")
    else:
        username = input("What username do you want to use for the God user? ")
        password = input("What password do you want to use for the God user? ")
        full_name = input("What name do you want to give the God user? (blank for the same as the username) ")
        if full_name == "":
            full_name = username
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)
        db.set_god_user(username, full_name, password_hash)
        print("")
        print("God username and password have been saved to the DB.")
