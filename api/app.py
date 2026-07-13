from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_PATH = "db/ev_stations.db"


def get_db():
    """Opens a connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us return rows as dictionaries
    return conn


@app.route("/")
def index():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "EV Data Pipeline API is running!",
        "endpoints": [
            "/stations",
            "/stations/<id>",
            "/cities",
            "/stats",
        ]
    })


@app.route("/stations")
def get_stations():
    """
    Returns all stations.
    Optional query params:
      - city: filter by city name (e.g. /stations?city=Berlin)
      - limit: max number of results (e.g. /stations?limit=10)
    """
    city  = request.args.get("city")
    limit = request.args.get("limit", 100, type=int)

    conn  = get_db()
    query = "SELECT * FROM stations"
    params = []

    if city:
        query += " WHERE city = ?"
        params.append(city.title())

    query += " LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/stations/<int:station_id>")
def get_station(station_id):
    """Returns a single station by ID."""
    conn = get_db()
    row  = conn.execute(
        "SELECT * FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "Station not found"}), 404

    return jsonify(dict(row))


@app.route("/cities")
def get_cities():
    """Returns a list of all unique cities in the database."""
    conn  = get_db()
    rows  = conn.execute(
        "SELECT DISTINCT city FROM stations ORDER BY city"
    ).fetchall()
    conn.close()

    return jsonify([row["city"] for row in rows])


@app.route("/stats")
def get_stats():
    """Returns summary statistics about the EV stations."""
    conn = get_db()

    total      = conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
    operational = conn.execute(
        "SELECT COUNT(*) FROM stations WHERE is_operational = 1"
    ).fetchone()[0]
    by_city    = conn.execute("""
        SELECT city, COUNT(*) as count
        FROM stations
        GROUP BY city
        ORDER BY count DESC
    """).fetchall()

    conn.close()

    return jsonify({
        "total_stations":       total,
        "operational_stations": operational,
        "offline_stations":     total - operational,
        "stations_by_city":     [dict(row) for row in by_city],
    })


if __name__ == "__main__":
    app.run(debug=True)