"""
Clean country_data.csv and save a simpler, analysis-ready version.

- Reads:  data/country_data.csv
- Creates: data/clean_country_data.csv

Steps:
1. Compute combined "life_expectancy"
2. Keep only relevant columns
3. Drop rows missing gdp_per_capita or life_expectancy
4. Add a new "continent" column (region → continent)
"""

from pathlib import Path
import pandas as pd

# ---------- REGION → CONTINENT MAPPING ----------
CONTINENT_MAP = {
    # Africa
    "Northern Africa": "Africa",
    "Middle Africa": "Africa",
    "Western Africa": "Africa",
    "Eastern Africa": "Africa",
    "Southern Africa": "Africa",

    # Asia
    "Southern Asia": "Asia",
    "Western Asia": "Asia",
    "South-Eastern Asia": "Asia",
    "Eastern Asia": "Asia",
    "Central Asia": "Asia",

    # Europe
    "Southern Europe": "Europe",
    "Western Europe": "Europe",
    "Eastern Europe": "Europe",
    "Northern Europe": "Europe",

    # Americas (combined)
    "Northern America": "North America",
    "Central America": "North America",
    "Caribbean": "North America",

    # South America
    "South America": "South America",

    # Oceania
    "Oceania": "Oceania",
    "Melanesia": "Oceania",
    "Micronesia": "Oceania",
    "Polynesia": "Oceania",
}

RAW_PATH = Path("data/country_data.csv")
CLEAN_PATH = Path("data/clean_country_data.csv")


def main():
    # ---- 1. Load raw file ----
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Input file not found: {RAW_PATH}")

    print(f"📥 Loading raw data from: {RAW_PATH}")
    df = pd.read_csv(RAW_PATH)

    print("Shape BEFORE cleaning:", df.shape)

    # ---- 2. Combine life expectancy columns ----
    if {"life_expectancy_male", "life_expectancy_female"}.issubset(df.columns):
        df["life_expectancy"] = df[["life_expectancy_male", "life_expectancy_female"]].mean(axis=1)
    else:
        df["life_expectancy"] = pd.NA

    # ---- 3. Keep only relevant columns ----
    keep_cols = [
        "name", "iso2", "region",
        "gdp", "gdp_per_capita", "population",
        "life_expectancy_male", "life_expectancy_female", "life_expectancy",
        "fertility", "internet_users", "unemployment",
        "urban_population_growth",
        "secondary_school_enrollment_female", "secondary_school_enrollment_male",
        "co2_emissions", "refugees",
    ]

    # Keep only columns that exist
    keep_cols = [c for c in keep_cols if c in df.columns]
    df_clean = df[keep_cols].copy()

    # ---- 4. Drop rows missing key variables ----
    df_clean = df_clean.dropna(subset=["gdp_per_capita", "life_expectancy"])

    # ---- 5. Add continent column ----
    df_clean["continent"] = df_clean["region"].map(CONTINENT_MAP).fillna("Other")

    print("Shape AFTER cleaning:", df_clean.shape)

    # ---- 6. Save cleaned data ----
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(CLEAN_PATH, index=False)

    print(f"✅ Wrote cleaned data to: {CLEAN_PATH}")


if __name__ == "__main__":
    main()
