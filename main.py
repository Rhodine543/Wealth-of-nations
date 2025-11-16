"""
Wealth of Nations – Exploratory Analysis on Clean Country Data

Loads the cleaned dataset (data/clean_country_data.csv)
and prints some basic info + correlations that we will later use
for multiple regression.
"""

from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/clean_country_data.csv")


def main():
    # 1) Load cleaned data
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find cleaned data: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    print("✅ Loaded CLEANED data")
    print("Shape (rows, columns):", df.shape)

    print("\n📌 Columns in the cleaned dataset:")
    print(list(df.columns))

    print("\nFirst 5 rows:")
    print(df.head())

    # 2) Pick variables we care about for regression
    #    Target: gdp_per_capita
    #    Predictors: life_expectancy, fertility, internet_users, unemployment, urban_population_growth
    cols = [
        "gdp_per_capita",
        "life_expectancy",
        "fertility",
        "internet_users",
        "unemployment",
        "urban_population_growth",
    ]

    # keep only columns that actually exist
    cols = [c for c in cols if c in df.columns]

    print("\n📈 Correlation of variables with gdp_per_capita:")
    corr = df[cols].corr()

    # print the correlation column for gdp_per_capita
    print(corr["gdp_per_capita"])


if __name__ == "__main__":
    main()
