CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE match (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    location TEXT NOT NULL,
    match_time TEXT NOT NULL,
    price INTEGER NOT NULL,
    info TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    host_user_id INTEGER NOT NULL,
    FOREIGN KEY (host_user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE match_participant (
    user_id INTEGER NOT NULL,
    match_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, match_id),
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (match_id) REFERENCES match (id) ON DELETE CASCADE
)