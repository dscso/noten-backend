CREATE TABLE IF NOT EXISTS user (
    UID       INTEGER  PRIMARY KEY AUTOINCREMENT,
    forename  STRING,
    surname   STRING,
    mail      STRING,
    birthdate DATETIME,
    password  TEXT
);

CREATE TABLE IF NOT EXISTS credentials (
    UID        INTEGER  NOT NULL,
    CLID       TEXT     NOT NULL,
    token      TEXT     NOT NULL,
    expiration DATETIME,
    PRIMARY KEY (
        CLID
    ),
    FOREIGN KEY (
        UID
    )
    REFERENCES user (UID) ON UPDATE CASCADE
                          ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS student (
    SID INTEGER NOT NULL,
    ANr STRING  NOT NULL,
    PRIMARY KEY (
        SID
    ),
    FOREIGN KEY (
        SID
    )
    REFERENCES user (UID) ON UPDATE CASCADE
                          ON DELETE CASCADE,
    FOREIGN KEY (
        ANr
    )
    REFERENCES affiliation (ANr) ON UPDATE CASCADE
                                 ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS affiliation (
    ANr STRING NOT NULL,
    PRIMARY KEY (
        ANr
    )
);

CREATE TABLE IF NOT EXISTS teacher (
    TID INTEGER NOT NULL,
    PRIMARY KEY (
        TID
    ),
    FOREIGN KEY (
        TID
    )
    REFERENCES user (UID) ON UPDATE CASCADE
                          ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS class (
    CNr STRING  NOT NULL,
    TID INTEGER,
    PRIMARY KEY (
        CNr
    ),
    FOREIGN KEY (
        CNr
    )
    REFERENCES affiliation (ANr) ON UPDATE CASCADE
                                 ON DELETE CASCADE,
    FOREIGN KEY (
        TID
    )
    REFERENCES teacher (TID) ON UPDATE CASCADE
                             ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS specific_lesson (
    SLID    INTEGER PRIMARY KEY AUTOINCREMENT,
    TID     INTEGER,
    CNr     STRING  NOT NULL,
    subject STRING,
    FOREIGN KEY (
        TID
    )
    REFERENCES teacher (TID) ON UPDATE CASCADE
                             ON DELETE CASCADE,
    FOREIGN KEY (
        CNr
    )
    REFERENCES class (Cnr) ON UPDATE CASCADE
                           ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS course (
    CID     INTEGER NOT NULL,
    TID     INTEGER,
    subject STRING,
    PRIMARY KEY (
        CID
    ),
    FOREIGN KEY (
        TID
    )
    REFERENCES teacher (TID) ON UPDATE CASCADE
                             ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS isincourse (
    SID INTEGER NOT NULL,
    CID INTEGER NOT NULL,
    FOREIGN KEY (
        SID
    )
    REFERENCES student (SID) ON UPDATE CASCADE
                             ON DELETE CASCADE,
    FOREIGN KEY (
        CID
    )
    REFERENCES course (CID) ON UPDATE CASCADE
                            ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tutorium (
    TNr STRING NOT NULL,
    CID STRING NOT NULL,
    PRIMARY KEY (
        TNr
    ),
    FOREIGN KEY (
        TNr
    )
    REFERENCES affiliation (ANr) ON UPDATE CASCADE
                                 ON DELETE CASCADE,
    FOREIGN KEY (
        CID
    )
    REFERENCES course (CID) ON UPDATE CASCADE
                            ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS marktype (
    MTID  INTEGER PRIMARY KEY AUTOINCREMENT,
    name  STRING,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS marks (
    MID  INTEGER PRIMARY KEY AUTOINCREMENT,
    SID  INTEGER NOT NULL,
    SLID INTEGER NOT NULL,
    MTID INTEGER,
    mark INTEGER NOT NULL,
    FOREIGN KEY (
        SID
    )
    REFERENCES student (SID) ON UPDATE CASCADE
                             ON DELETE CASCADE,
    FOREIGN KEY (
        SLID
    )
    REFERENCES specific_lesson (SLID) ON UPDATE CASCADE
                                      ON DELETE CASCADE,
    FOREIGN KEY (
        MTID
    )
    REFERENCES marktype (MTID) ON UPDATE CASCADE
                               ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS pointtype (
    PTID  INTEGER PRIMARY KEY AUTOINCREMENT,
    name  STRING,
    value FLOAT
);

CREATE TABLE IF NOT EXISTS points (
    PID    INTEGER PRIMARY KEY AUTOINCREMENT,
    SID    INTEGER NOT NULL,
    CID    INTEGER NOT NULL,
    PTID   INTEGER,
    points INTEGER NOT NULL,
    FOREIGN KEY (
        SID
    )
    REFERENCES student (SID) ON UPDATE CASCADE
                             ON DELETE CASCADE,
    FOREIGN KEY (
        CID
    )
    REFERENCES course (CID) ON UPDATE CASCADE
                            ON DELETE CASCADE,
    FOREIGN KEY (
        PTID
    )
    REFERENCES pointtype (PTID) ON UPDATE CASCADE
                                ON DELETE CASCADE
);
