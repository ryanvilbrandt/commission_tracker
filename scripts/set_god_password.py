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

username = input("What's the username you want to use for the God user? ")
password = input("What's the password you want to use for the God user? ")
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password.encode(), salt)

try:
    db_obj = Db()
except FileNotFoundError:
    build_db.main()
    db_obj = Db()

with db_obj as db:
    db.set_god_user(username, password_hash)

print("")
print("Username and password have been saved to the DB.")
