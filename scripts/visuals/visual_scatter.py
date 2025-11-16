import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean_country_data.csv")

def scatter_plot(x, y, filename):
    plt.figure(figsize=(8,6))
    sns.scatterplot(data=df, x=x, y=y, hue="continent")
    plt.title(f"{y} vs {x} by Continent")
    plt.savefig(f"outputs/{filename}")
    plt.close()
    print(f"✔️ Saved: outputs/{filename}")

scatter_plot("life_expectancy", "gdp_per_capita", "gdp_vs_life_expectancy_continents.png")
scatter_plot("internet_users", "gdp_per_capita", "gdp_vs_internet_users_continents.png")
scatter_plot("fertility", "gdp_per_capita", "gdp_vs_fertility_continents.png")
