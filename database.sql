CREATE TABLE User (
    UID      INTEGER PRIMARY KEY AUTOINCREMENT,
    Mail     TEXT    UNIQUE,
    Password TEXT
);
