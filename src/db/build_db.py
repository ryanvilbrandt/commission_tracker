import os
import sqlite3
from sqlite3 import Cursor

import bcrypt


def open_db():
    os.makedirs("database_files", exist_ok=True)
    db = sqlite3.connect("database_files/main.db")
    cur = db.cursor()
    return db, cur


def drop_tables(cur: Cursor):
    print("Dropping all tables in database...")

    sql = """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS commissions;
    """
    cur.executescript(sql)

    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    tables = cur.execute(sql).fetchall()
    if tables:
        raise Exception(f"Some tables were not deleted: {tables}")


def run_ddl(cur: Cursor, ddl_filepath: str):
    with open(ddl_filepath) as f:
        cur.executescript(f.read())


def set_system_user_password(cur: Cursor, password: str):
    sql = """
        UPDATE users SET password_hash=? WHERE id=-1;
    """
    pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur.execute(sql, [pw])


def show_tables(cur):
    sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    for row in cur.execute(sql).fetchall():
        print(row[0])


def main():
    ddl_filepath = "src/db/build_db_kofi.ddl"

    db, cur = open_db()

    # drop_tables(cur)
    run_ddl(cur, ddl_filepath)
    set_system_user_password(cur, os.getenv("SERVICE_ACCOUNT_PASSWORD", default=""))
    db.commit()

    show_tables(cur)

    db.close()


if __name__ == "__main__":
    raise Exception("Run scripts/set_god_password.py instead.")
    # os.chdir("../..")
    # main()
