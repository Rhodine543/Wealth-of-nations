"""Plotting helpers for the Wealth of Nations project.

This module exposes two functions:
- plot_country_timeseries: line chart of life expectancy over time for countries
- plot_year_distribution: histogram of life expectancy for a single year

These helpers are importable without running any plotting at import time.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Union

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

PathLike = Union[str, Path]


def plot_country_timeseries(df: pd.DataFrame, countries: Iterable[str], out_path: PathLike) -> None:
	"""Plot life expectancy over time for selected countries and save to out_path.

	Parameters
	- df: DataFrame with columns ["country", "year", "life_expectancy_years"].
	- countries: iterable of country names to include.
	- out_path: target file path (PNG will be written).
	"""
	p = Path(out_path)
	p.parent.mkdir(parents=True, exist_ok=True)
	df_sub = df[df["country"].isin(countries)]
	plt.figure(figsize=(8, 5))
	sns.lineplot(data=df_sub, x="year", y="life_expectancy_years", hue="country")
	plt.title("Life expectancy over time")
	plt.tight_layout()
	plt.savefig(p, dpi=150)
	plt.close()


def plot_year_distribution(df: pd.DataFrame, year: int, out_path: PathLike) -> None:
	"""Plot a distribution (histogram) of life expectancy for a given year.

	Parameters
	- df: DataFrame with columns ["country", "year", "life_expectancy_years"].
	- year: integer year to filter the dataframe.
	- out_path: target file path for the PNG.
	"""
	p = Path(out_path)
	p.parent.mkdir(parents=True, exist_ok=True)
	df_year = df[df["year"] == year]
	plt.figure(figsize=(7, 4))
	sns.histplot(df_year["life_expectancy_years"].dropna(), bins=30)
	plt.title(f"Life expectancy distribution, {year}")
	plt.tight_layout()
	plt.savefig(p, dpi=150)
	plt.close()


__all__ = ["plot_country_timeseries", "plot_year_distribution"]

