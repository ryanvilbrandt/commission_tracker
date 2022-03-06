import os
import sqlite3


def open_db():
    os.makedirs("database_files", exist_ok=True)
    db = sqlite3.connect("database_files/main.db")
    cur = db.cursor()
    return db, cur


def get_version(cur):
    sql = "SELECT version FROM version"
    try:
        version = cur.execute(sql).fetchone()[0]
    except sqlite3.OperationalError:
        return 0
    else:
        return version


def set_version(cur, v):
    sql = "UPDATE version SET version = ?"
    cur.execute(sql, [v])
    print(f"Set version to {v}")


def drop_tables(cur):
    print("Dropping all tables in database...")

    sql = """
        DROP TABLE IF EXISTS version;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS commissions;
    """
    cur.executescript(sql)

    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    tables = cur.execute(sql).fetchall()
    if tables:
        raise Exception(f"Some tables were not deleted: {tables}")


def create_tables(cur):
    if get_version(cur) >= 1:
        print("Skipping creating tables...")
        return

    print("Creating tables...")

    # Create version table and initialize with 0
    sql = """
    CREATE TABLE IF NOT EXISTS version (
        version INTEGER PRIMARY KEY
    );
    INSERT INTO version (version) VALUES (0);
    """
    cur.executescript(sql)

    sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        full_name TEXT DEFAULT '',
        password_hash TEXT,
        role TEXT DEFAULT 'user'
    );
    CREATE TABLE IF NOT EXISTS commissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP,
        name TEXT DEFAULT '',
        email TEXT DEFAULT '',
        twitch TEXT DEFAULT '',
        twitter TEXT DEFAULT '',
        discord TEXT DEFAULT '',
        reference_images TEXT DEFAULT '',
        description TEXT DEFAULT '',
        expression TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        artist_choice TEXT DEFAULT '',
        if_queue_is_full TEXT DEFAULT '',
        assigned_to INTEGER DEFAULT NULL,
        allow_any_artist BOOLEAN DEFAULT FALSE,
        hidden BOOLEAN DEFAULT FALSE,
        accepted BOOLEAN DEFAULT FALSE,
        invoiced BOOLEAN DEFAULT FALSE,
        paid BOOLEAN DEFAULT FALSE,
        finished BOOLEAN DEFAULT FALSE,
        channel_name TEXT DEFAULT NULL,
        message_id INTEGER DEFAULT NULL,
        counter INTEGER DEFAULT NULL,
        UNIQUE (timestamp, email) ON CONFLICT IGNORE
    );
    PRAGMA case_sensitive_like=ON;
    """
    cur.executescript(sql)

    set_version(cur, 1)


def show_tables(cur):
    sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    for row in cur.execute(sql).fetchall():
        print(row[0])


def main():
    db, cur = open_db()

    drop_tables(cur)
    create_tables(cur)
    db.commit()

    show_tables(cur)

    db.close()


if __name__ == "__main__":
    raise Exception("Run scripts/set_god_password.py instead.")
    # os.chdir("../..")
    # main()
