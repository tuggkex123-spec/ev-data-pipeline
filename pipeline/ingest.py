import pandas as pd

def fetch_ev_stations(filepath="data/ev_stations.csv"):
    """
    Loads EV charging station data from a local CSV file.
    """
    print(f"Loading EV station data from {filepath}...")

    df = pd.read_csv(filepath)
    print(f"✅ Loaded {len(df)} stations.")
    return df


def parse_stations(df):
    """
    Cleans column types and ensures the DataFrame is properly formatted.
    """
    df["is_operational"] = df["is_operational"].astype(bool)
    df["capacity"]       = pd.to_numeric(df["capacity"],  errors="coerce")
    df["power_kw"]       = pd.to_numeric(df["power_kw"],  errors="coerce")
    df["latitude"]       = pd.to_numeric(df["latitude"],  errors="coerce")
    df["longitude"]      = pd.to_numeric(df["longitude"], errors="coerce")

    print(f"✅ Parsed and typed {len(df)} stations.")
    return df


if __name__ == "__main__":
    df = fetch_ev_stations()
    df = parse_stations(df)
    print(df.head())
    print(f"\nColumns: {list(df.columns)}")