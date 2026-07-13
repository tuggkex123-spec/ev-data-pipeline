import pandas as pd

def transform(df):
    """
    Cleans and enriches the raw EV station DataFrame.
    """
    print("Transforming data...")

    # 1. Drop rows where critical fields are missing
    before = len(df)
    df = df.dropna(subset=["latitude", "longitude", "city"])
    print(f"  → Dropped {before - len(df)} rows with missing location data.")

    # 2. Standardize text columns to title case
    df["city"]     = df["city"].str.strip().str.title()
    df["operator"] = df["operator"].str.strip().str.title()
    df["network"]  = df["network"].str.strip().str.title()

    # 3. Filter out stations with unrealistic power values
    before = len(df)
    df = df[df["power_kw"] > 0]
    print(f"  → Dropped {before - len(df)} rows with invalid power values.")

    # 4. Add a power category column
    def categorize_power(kw):
        if kw <= 22:
            return "Slow"
        elif kw <= 100:
            return "Fast"
        else:
            return "Ultra-Fast"

    df["power_category"] = df["power_kw"].apply(categorize_power)

    # 5. Convert last_updated to datetime
    df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")

    # 6. Add a flag for high capacity stations
    df["is_high_capacity"] = df["capacity"] >= 10

    print(f"✅ Transformation complete. {len(df)} stations remaining.")
    return df


if __name__ == "__main__":
    from ingest import fetch_ev_stations, parse_stations
    df = fetch_ev_stations()
    df = parse_stations(df)
    df = transform(df)
    print(df[["name", "city", "power_kw", "power_category", "is_high_capacity"]].head(10))