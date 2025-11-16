import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/clean_country_data.csv")

# Bar chart of GDP per capita by continent
continent_avg = df.groupby("continent")["gdp_per_capita"].mean().sort_values()

plt.figure(figsize=(10,6))
sns.barplot(x=continent_avg.index, y=continent_avg.values)
plt.title("Average GDP per Capita by Continent")
plt.ylabel("GDP per Capita")
plt.xlabel("Continent")

plt.tight_layout()
plt.savefig("outputs/continent_gdp_bar.png")
plt.close()
print("✔️ Saved: outputs/continent_gdp_bar.png")

