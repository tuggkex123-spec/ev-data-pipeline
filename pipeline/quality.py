import pandas as pd

def run_quality_checks(df):
    """
    Runs a series of data quality checks on the EV station DataFrame.
    Prints a report and returns True if all checks pass, False otherwise.
    """
    print("Running data quality checks...")
    passed = True
    issues = []

    # Check 1 — No duplicate station IDs
    duplicates = df["id"].duplicated().sum()
    if duplicates > 0:
        issues.append(f"  ❌ Found {duplicates} duplicate station IDs.")
        passed = False
    else:
        print("  ✅ No duplicate station IDs.")

    # Check 2 — No missing coordinates
    missing_coords = df[["latitude", "longitude"]].isnull().any(axis=1).sum()
    if missing_coords > 0:
        issues.append(f"  ❌ {missing_coords} stations have missing coordinates.")
        passed = False
    else:
        print("  ✅ No missing coordinates.")

    # Check 3 — Latitude and longitude are in valid range
    invalid_lat = df[(df["latitude"] < -90)  | (df["latitude"] > 90)].shape[0]
    invalid_lon = df[(df["longitude"] < -180) | (df["longitude"] > 180)].shape[0]
    if invalid_lat > 0 or invalid_lon > 0:
        issues.append(f"  ❌ {invalid_lat} invalid latitudes, {invalid_lon} invalid longitudes.")
        passed = False
    else:
        print("  ✅ All coordinates are in valid range.")

    # Check 4 — Power values are positive
    invalid_power = df[df["power_kw"] <= 0].shape[0]
    if invalid_power > 0:
        issues.append(f"  ❌ {invalid_power} stations have invalid power values.")
        passed = False
    else:
        print("  ✅ All power values are positive.")

    # Check 5 — No missing city names
    missing_city = df["city"].isnull().sum()
    if missing_city > 0:
        issues.append(f"  ❌ {missing_city} stations have missing city names.")
        passed = False
    else:
        print("  ✅ No missing city names.")

    # Check 6 — Capacity is a positive number
    invalid_capacity = df[df["capacity"] <= 0].shape[0]
    if invalid_capacity > 0:
        issues.append(f"  ❌ {invalid_capacity} stations have invalid capacity.")
        passed = False
    else:
        print("  ✅ All capacity values are positive.")

    # Final report
    print("\n--- Quality Check Report ---")
    if passed:
        print("✅ All checks passed! Data is ready for loading.")
    else:
        print("⚠️  Some checks failed:")
        for issue in issues:
            print(issue)

    return passed


if __name__ == "__main__":
    from ingest import fetch_ev_stations, parse_stations
    from transform import transform
    df = fetch_ev_stations()
    df = parse_stations(df)
    df = transform(df)
    run_quality_checks(df)