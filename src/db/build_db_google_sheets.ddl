CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    full_name TEXT DEFAULT '',
    password_hash TEXT,
    role TEXT DEFAULT 'user',
    is_artist BOOLEAN DEFAULT FALSE
);
CREATE TABLE IF NOT EXISTS commissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP,
    name TEXT DEFAULT '',
    email TEXT DEFAULT '',
    twitch TEXT DEFAULT '',
    twitter TEXT DEFAULT '',
    discord TEXT DEFAULT '',
    num_characters TEXT DEFAULT '',
    reference_images TEXT DEFAULT '',
    description TEXT DEFAULT '',
    expression TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    artist_choice TEXT DEFAULT '',
    if_queue_is_full TEXT DEFAULT '',
    assigned_to INTEGER DEFAULT -1,
    allow_any_artist BOOLEAN DEFAULT FALSE,
    accepted BOOLEAN DEFAULT FALSE,
    invoiced BOOLEAN DEFAULT FALSE,
    paid BOOLEAN DEFAULT FALSE,
    finished BOOLEAN DEFAULT FALSE,
    UNIQUE (timestamp, email) ON CONFLICT IGNORE
);
PRAGMA case_sensitive_like=ON;

-- The password hash should be set by the script that's calling the DDL file
INSERT INTO users(id, username, full_name, password_hash, role)
VALUES (-1, 'unassigned', 'Unassigned', null, 'system');