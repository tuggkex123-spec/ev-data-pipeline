-- EV Charging Station Database Schema

CREATE TABLE IF NOT EXISTS countries (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE,
    code    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS connection_types (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS stations (
    id                  INTEGER PRIMARY KEY,
    name                TEXT NOT NULL,
    address             TEXT,
    city                TEXT,
    postcode            TEXT,
    country_id          INTEGER REFERENCES countries(id),
    latitude            REAL,
    longitude           REAL,
    num_points          INTEGER,
    is_operational      BOOLEAN DEFAULT TRUE,
    last_updated        TEXT
);

CREATE TABLE IF NOT EXISTS connections (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    station_id          INTEGER REFERENCES stations(id),
    connection_type_id  INTEGER REFERENCES connection_types(id),
    power_kw            REAL,
    quantity            INTEGER
);