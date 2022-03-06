import os

import bcrypt

from src.db import build_db
from src.db.db import Db

dirname = os.path.dirname(__file__)
cwd = os.getcwd().replace("\\", "/")
if dirname == cwd:
    os.chdir("..")

print("This script will set the God user and their password hash in the DB.")
print("")

username = input("What username do you want to use for the God user? ")
password = input("What password do you want to use for the God user? ")
full_name = input("What name do you want to give the God user? (blank for the same as the username) ")
if full_name == "":
    full_name = username
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password.encode(), salt)

try:
    db_obj = Db()
except FileNotFoundError:
    build_db.main()
    db_obj = Db()

with db_obj as db:
    db.set_god_user(username, full_name, password_hash)

print("")
print("Username and password have been saved to the DB.")
