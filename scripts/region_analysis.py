import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/clean_country_data.csv")

# Variables to analyze
vars_to_check = [
    "life_expectancy",
    "internet_users",
    "fertility",
    "unemployment",
    "urban_population_growth"
]

# Store results
corr_results = []

# Compute correlation per region
for region, group in df.groupby("region"):
    for var in vars_to_check:
        corr = group[var].corr(group["gdp_per_capita"])
        corr_results.append({
            "region": region,
            "variable": var,
            "correlation": corr
        })

corr_df = pd.DataFrame(corr_results)

# Save correlation table
corr_df.to_csv("outputs/regional_correlations.csv", index=False)
print("✅ Saved regional correlation table -> outputs/regional_correlations.csv")

# --- Visualization 1: heatmap style (variables × regions) ---
pivot_df = corr_df.pivot(index="variable", columns="region", values="correlation")

plt.figure(figsize=(14, 6))
sns.heatmap(pivot_df, annot=True, cmap="coolwarm", center=0)
plt.title("Correlation of Variables with GDP per Capita by Region")
plt.tight_layout()
plt.savefig("outputs/regional_heatmap.png", dpi=150)
plt.close()
print("📊 Saved heatmap -> outputs/regional_heatmap.png")

# --- Visualization 2: bar chart for each variable ---
plt.figure(figsize=(12, 6))
sns.barplot(data=corr_df, x="variable", y="correlation", hue="region")
plt.axhline(0, color="black", linewidth=1)
plt.title("Strength of Correlations by Region")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/regional_bars.png", dpi=150)
plt.close()
print("📉 Saved comparison bar plot -> outputs/regional_bars.png")
