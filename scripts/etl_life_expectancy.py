"""ETL utilities for the Wealth of Nations project.

Contains functions to load the raw CSV, build a simplified table (country, year, life_expectancy_years)
and save the result.
"""
from pathlib import Path
import pandas as pd
from typing import Union


def load_raw(path: Union[str, Path]) -> pd.DataFrame:
    """Load raw CSV into a pandas DataFrame.

    Args:
        path: path to the raw CSV file.

    Returns:
        pandas.DataFrame
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")
    df = pd.read_csv(p)
    return df


def build_simple(df: pd.DataFrame) -> pd.DataFrame:
    """Build a simplified DataFrame with columns: country, year, life_expectancy_years.

    Prefers numeric values in `FactValueNumeric`. Falls back to extracting numbers from `Value`.
    """
    df = df.copy()
    # Prefer FactValueNumeric
    if 'FactValueNumeric' in df.columns:
        df['life_numeric'] = pd.to_numeric(df['FactValueNumeric'], errors='coerce')
    else:
        df['life_numeric'] = pd.NA

    if df['life_numeric'].isna().all() and 'Value' in df.columns:
        extracted = df['Value'].astype(str).str.extract(r'([0-9]+\.?[0-9]*)')
        df['life_numeric'] = pd.to_numeric(extracted[0], errors='coerce')

    # Find country and year columns
    country_col = None
    for c in ['Location','Country','location','country','ParentLocation']:
        if c in df.columns:
            country_col = c
            break

    year_col = None
    for c in ['Period','Year','period','year']:
        if c in df.columns:
            year_col = c
            break

    if country_col is None or year_col is None:
        raise ValueError('Could not find country or year columns in input DataFrame')

    out = df[[country_col, year_col, 'life_numeric']].rename(columns={country_col:'country', year_col:'year', 'life_numeric':'life_expectancy_years'})
    out = out.dropna(subset=['life_expectancy_years']).copy()
    out['year'] = pd.to_numeric(out['year'], errors='coerce').astype('Int64')
    return out


def save(df: pd.DataFrame, out_path: Union[str, Path]):
    """Save DataFrame to CSV and ensure directory exists."""
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False)


if __name__ == '__main__':
    # small CLI for manual running
    import argparse
    parser = argparse.ArgumentParser(description='Run ETL for life expectancy CSV')
    parser.add_argument('--in', dest='inpath', default='data/life_expectancy.csv', help='Raw input CSV')
    parser.add_argument('--out', dest='outpath', default='data/life_expectancy_simple.csv', help='Output CSV')
    args = parser.parse_args()
    df = load_raw(args.inpath)
    simple = build_simple(df)
    save(simple, args.outpath)
    print(f'Wrote simplified CSV: {args.outpath} (rows={len(simple)})')
