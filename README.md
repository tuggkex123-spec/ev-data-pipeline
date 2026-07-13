# EV Charging Station Data Pipeline

![CI](https://github.com/tuggkex123-spec/ev-data-pipeline/actions/workflows/ci.yml/badge.svg)

An end-to-end data engineering pipeline that ingests, transforms, validates,
and serves EV charging station data across Germany.
Built as a portfolio project targeting real-world data engineering practices.

---

## Architecture
```
CSV Data Source
      │
      ▼
┌─────────────┐
│   Ingest    │  Loads raw CSV data into a pandas DataFrame
└─────────────┘
      │
      ▼
┌─────────────┐
│  Transform  │  Cleans, enriches, and categorizes the data
└─────────────┘
      │
      ▼
┌─────────────┐
│   Quality   │  Runs 6 data quality checks before loading
└─────────────┘
      │
      ▼
┌─────────────┐
│    Load     │  Writes clean data into a normalized SQLite database
└─────────────┘
      │
      ▼
┌─────────────┐
│  Flask API  │  Serves the data via REST endpoints
└─────────────┘
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core pipeline language |
| Pandas | Data transformation |
| SQLite + SQLAlchemy | Database storage |
| Flask | REST API |
| Pytest | Unit testing |
| GitHub Actions | CI/CD — runs tests on every push |

---

## Project Structure
```
ev-data-pipeline/
├── .github/workflows/
│   └── ci.yml            # GitHub Actions CI/CD
├── api/
│   └── app.py            # Flask REST API
├── data/
│   └── ev_stations.csv   # Source dataset (200 EV stations, Germany)
├── db/
│   ├── schema.sql        # Normalized SQL schema
│   └── ev_stations.db    # SQLite database (generated)
├── pipeline/
│   ├── ingest.py         # Extract: loads CSV into DataFrame
│   ├── transform.py      # Transform: cleans and enriches data
│   ├── quality.py        # Validate: 6 data quality checks
│   └── load.py           # Load: writes to SQLite database
├── tests/
│   └── test_pipeline.py  # 8 unit tests
└── README.md
```

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/tuggkex123-spec/ev-data-pipeline.git
cd ev-data-pipeline
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install requests pandas sqlalchemy flask pytest
```

### 4. Run the full pipeline
```bash
python pipeline/load.py
```

### 5. Start the Flask API
```bash
python api/app.py
```

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Health check |
| `GET /stations` | All stations (supports `?city=Berlin&limit=10`) |
| `GET /stations/<id>` | Single station by ID |
| `GET /cities` | List of all cities |
| `GET /stats` | Summary statistics |

---

## Data Quality Checks

The pipeline runs 6 automated checks before loading data:

- ✅ No duplicate station IDs
- ✅ No missing coordinates
- ✅ All coordinates in valid range
- ✅ All power values are positive
- ✅ No missing city names
- ✅ All capacity values are positive

If any check fails, the pipeline stops and does not load bad data.

---

## Running Tests
```bash
python -m pytest tests/ -v
```

8 unit tests covering transformation logic and data quality validation.

---

## Key Concepts Demonstrated

- **ETL Pipeline** — Extract, Transform, Load pattern
- **Data Quality Assurance** — validation before loading
- **Normalized SQL Schema** — 4 related tables with foreign keys
- **REST API** — Flask serving pipeline results
- **CI/CD** — automated testing on every push via GitHub Actions