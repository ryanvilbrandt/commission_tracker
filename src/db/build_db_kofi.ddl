CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    is_active TEXT DEFAULT TRUE,
    full_name TEXT DEFAULT '',
    password_hash TEXT,
    role TEXT DEFAULT 'user',
    is_artist BOOLEAN DEFAULT FALSE,
    queue_open BOOLEAN DEFAULT FALSE
);
CREATE TABLE commissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_ts TIMESTAMP,
    updated_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    name TEXT DEFAULT '',
    email TEXT DEFAULT '',
    price TEXT DEFAULT '',
    message TEXT DEFAULT '',
    url TEXT DEFAULT '',
    num_characters TEXT DEFAULT NULL,
    preferred_artist INTEGER DEFAULT NULL,
    is_exclusive BOOLEAN DEFAULT NULL,
    assigned_to INTEGER DEFAULT -1,
    finished BOOLEAN DEFAULT FALSE,
    uploaded_filename TEXT DEFAULT NULL,
    emailed BOOLEAN DEFAULT FALSE,
    removed BOOLEAN DEFAULT FALSE,
    refunded BOOLEAN DEFAULT FALSE,
    archived BOOLEAN DEFAULT FALSE,
    UNIQUE (created_ts, email) ON CONFLICT IGNORE
);
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    commission_id INTEGER,
    user_id INTEGER,
    created_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text TEXT
);
PRAGMA case_sensitive_like=ON;

-- The password hash should be set by the script calling the DDL file
INSERT INTO users(id, username, full_name, password_hash, role)
VALUES (-1, 'unassigned', 'Unassigned', null, 'system');
