CREATE TABLE IF NOT EXISTS headlines (
    id                  INTEGER PRIMARY KEY,
    filename            VARCHAR(4096) NOT NULL,
    parent              TEXT NOT NULL,
    todo                VARCHAR(10),
    heading             TEXT NOT NULL,
    category            VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS headline_tags (
    headline_id         INTEGER NOT NULL,
    tag                 VARCHAR(20) NOT NULL,

    CONSTRAINT hdl_tag UNIQUE(headline_id, tag),
    FOREIGN KEY (headline_id)
        REFERENCES headlines(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS clocks (
    headline_id         INTEGER NOT NULL,
    dt_start            DATETIME NOT NULL,
    dt_end              DATETIME NOT NULL,
    duration_min        INTEGER NOT NULL
                        GENERATED ALWAYS AS (CAST ((
                            julianday(dt_end) - julianday(dt_start)
                        ) * 24 * 60 * 60 AS INTEGER)) STORED,

    FOREIGN KEY (headline_id)
        REFERENCES headlines(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
