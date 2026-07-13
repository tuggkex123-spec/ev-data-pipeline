import sqlite3
import pandas as pd
import os

DB_PATH = "db/ev_stations.db"

def init_database():
    """
    Creates the database and tables from our schema file.
    """
    print("Initializing database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open("db/schema.sql", "r") as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("✅ Database initialized.")


def load_stations(df):
    """
    Loads the cleaned DataFrame into the SQLite database.
    """
    print("Loading stations into database...")
    conn = sqlite3.connect(DB_PATH)

    # Load countries first
    countries = df[["country_code"]].drop_duplicates()
    countries["name"] = "Germany"
    countries = countries.rename(columns={"country_code": "code"})

    for _, row in countries.iterrows():
        conn.execute("""
            INSERT OR IGNORE INTO countries (name, code)
            VALUES (?, ?)
        """, (row["name"], row["code"]))

    # Load connection types
    for socket_type in df["socket_type"].dropna().unique():
        conn.execute("""
            INSERT OR IGNORE INTO connection_types (name)
            VALUES (?)
        """, (socket_type,))

    # Load stations
    for _, row in df.iterrows():
        country_id = conn.execute(
            "SELECT id FROM countries WHERE code = ?", (row["country_code"],)
        ).fetchone()

        conn.execute("""
            INSERT OR REPLACE INTO stations
                (id, name, address, city, postcode, country_id,
                 latitude, longitude, num_points, is_operational, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["id"],
            row["name"],
            None,
            row["city"],
            row["postcode"],
            country_id[0] if country_id else None,
            row["latitude"],
            row["longitude"],
            row["capacity"],
            row["is_operational"],
            str(row["last_updated"]),
        ))

    conn.commit()

    # Confirm how many rows were loaded
    count = conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
    conn.close()
    print(f"✅ Loaded {count} stations into the database.")


if __name__ == "__main__":
    from ingest import fetch_ev_stations, parse_stations
    from transform import transform
    from quality import run_quality_checks

    df = fetch_ev_stations()
    df = parse_stations(df)
    df = transform(df)

    if run_quality_checks(df):
        init_database()
        load_stations(df)
    else:
        print("⚠️ Pipeline stopped — data quality checks failed.")