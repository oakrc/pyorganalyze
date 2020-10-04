DROP TABLE IF EXISTS clocks;
CREATE TABLE IF NOT EXISTS clocks (
    headline_id         INTEGER NOT NULL,
    clock_start         DATETIME NOT NULL,
    duration_min        INTEGER NOT NULL,
);

DROP TABLE IF EXISTS headlines;
CREATE TABLE IF NOT EXISTS headlines (
    id                  INTEGER PRIMARY KEY,
    filename            VARCHAR(4096) NOT NULL,
    parent              TEXT NOT NULL,
    category            VARCHAR(20) NOT NULL,
    todo_state          VARCHAR(10) NOT NULL
);

DROP TABLE IF EXISTS headline_tags;
CREATE TABLE IF NOT EXISTS headline_tags (
    headline_id         INTEGER NOT NULL,
    tag                 VARCHAR(20) NOT NULL
);
