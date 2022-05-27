CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    full_name TEXT DEFAULT '',
    password_hash TEXT,
    role TEXT DEFAULT 'user',
    is_artist BOOLEAN DEFAULT FALSE,
    queue_open BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS commissions (
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
    accepted BOOLEAN DEFAULT FALSE,
    invoiced BOOLEAN DEFAULT TRUE,
    paid BOOLEAN DEFAULT TRUE,
    finished BOOLEAN DEFAULT FALSE,
    uploaded_filename TEXT DEFAULT NULL,
    archived BOOLEAN DEFAULT FALSE,
    removed BOOLEAN DEFAULT FALSE,
    refunded BOOLEAN DEFAULT FALSE,
    UNIQUE (created_ts, email) ON CONFLICT IGNORE
);
PRAGMA case_sensitive_like=ON;

-- The password hash should be set by the script that's calling the DDL file
INSERT INTO users(id, username, full_name, password_hash, role)
VALUES (-1, 'unassigned', 'Unassigned', null, 'system');
