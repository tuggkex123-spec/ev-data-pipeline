import pytest
import pandas as pd
import sys
import os

# Make sure Python can find our pipeline folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pipeline.transform import transform
from pipeline.quality import run_quality_checks


def make_sample_df():
    """Creates a small sample DataFrame for testing."""
    return pd.DataFrame([
        {
            "id": 1, "name": "Station A", "city": "berlin",
            "postcode": "10115", "country_code": "DE",
            "latitude": 52.52, "longitude": 13.40,
            "operator": "enbw", "network": "enbw",
            "socket_type": "CCS", "capacity": 5,
            "power_kw": 150, "is_operational": True,
            "last_updated": "2026-01-01"
        },
        {
            "id": 2, "name": "Station B", "city": "munich",
            "postcode": "80331", "country_code": "DE",
            "latitude": 48.13, "longitude": 11.58,
            "operator": "ionity", "network": "ionity",
            "socket_type": "Type2", "capacity": 12,
            "power_kw": 22, "is_operational": False,
            "last_updated": "2026-02-01"
        },
        {
            "id": 3, "name": "Station C", "city": "hamburg",
            "postcode": "20095", "country_code": "DE",
            "latitude": 53.55, "longitude": 10.00,
            "operator": "allego", "network": "roaming",
            "socket_type": "CHAdeMO", "capacity": 3,
            "power_kw": 50, "is_operational": True,
            "last_updated": "2026-03-01"
        },
    ])


# --- Transform tests ---

def test_city_is_title_cased():
    df = transform(make_sample_df())
    assert df["city"].iloc[0] == "Berlin"
    assert df["city"].iloc[1] == "Munich"


def test_power_category_ultra_fast():
    df = transform(make_sample_df())
    assert df["power_category"].iloc[0] == "Ultra-Fast"


def test_power_category_slow():
    df = transform(make_sample_df())
    assert df["power_category"].iloc[1] == "Slow"


def test_power_category_fast():
    df = transform(make_sample_df())
    assert df["power_category"].iloc[2] == "Fast"


def test_high_capacity_flag():
    df = transform(make_sample_df())
    assert df["is_high_capacity"].iloc[1] == True   # capacity 12 >= 10
    assert df["is_high_capacity"].iloc[0] == False  # capacity 5 < 10


def test_last_updated_is_datetime():
    df = transform(make_sample_df())
    assert pd.api.types.is_datetime64_any_dtype(df["last_updated"])


# --- Quality check tests ---

def test_quality_checks_pass_on_clean_data():
    df = transform(make_sample_df())
    result = run_quality_checks(df)
    assert result == True


def test_quality_checks_fail_on_duplicate_ids():
    df = make_sample_df()
    df.loc[1, "id"] = 1  # make a duplicate ID
    df = transform(df)
    result = run_quality_checks(df)
    assert result == False