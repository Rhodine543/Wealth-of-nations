"""Runner script that creates plots for the Wealth of Nations project.

This file is intentionally a small runner that imports plotting helpers from
`scripts.plot_helpers` and writes two example plots to `outputs/`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

from scripts.plot_helpers import plot_country_timeseries, plot_year_distribution


def main() -> int:
    data_path = Path("data") / "life_expectancy_simple.csv"
    if not data_path.exists():
        print(f"Error: data file not found: {data_path}", file=sys.stderr)
        return 2

    df = pd.read_csv(data_path)

    # Plot 1: Line chart for selected countries
    plot_country_timeseries(
        df,
        countries=["Kenya", "France", "United States"],
        out_path=Path("outputs") / "life_trends.png",
    )

    # Plot 2: Histogram for a selected year
    plot_year_distribution(
        df,
        year=2020,
        out_path=Path("outputs") / "life_distribution_2020.png",
    )

    print("✅ Plots created! Check the outputs folder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
