import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/clean_country_data.csv")

# Variables whose correlation with gdp_per_capita we care about
variables = [
    "life_expectancy",
    "internet_users",
    "fertility",
    "unemployment",
    "urban_population_growth",
]

rows = []

# For each continent, compute correlation with gdp_per_capita
for continent, sub in df.groupby("continent"):
    sub_clean = sub[variables + ["gdp_per_capita"]].dropna()
    if len(sub_clean) < 3:
        # Skip continents with too few data points
        continue

    corr_series = sub_clean.corr()["gdp_per_capita"].loc[variables]
    corr_series.name = continent
    rows.append(corr_series)

# Combine into a DataFrame: rows = continents, columns = variables
continent_corr = pd.DataFrame(rows)

print("Correlation with GDP per capita by continent:")
print(continent_corr)

# Plot heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(continent_corr, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation with GDP per Capita by Continent")
plt.xlabel("Variable")
plt.ylabel("Continent")
plt.tight_layout()
plt.savefig("outputs/continent_heatmap.png")
plt.close()
print("✔️ Saved: outputs/continent_heatmap.png")
