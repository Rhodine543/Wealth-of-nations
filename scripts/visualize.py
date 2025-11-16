import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path


def scatter_plot(df, x, y, out_path):
    """
    Creates a scatter plot with a regression line.
    """
    out = Path(out_path)
    out.parent.mkdir(exist_ok=True, parents=True)

    plt.figure(figsize=(7, 5))
    sns.regplot(data=df, x=x, y=y, scatter_kws={"alpha": 0.6})
    plt.title(f"{y} vs {x}")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()


def visualize_all(df):
    """
    Creates the three main visualizations for the project.
    """

    scatter_plot(df, x="internet_users", y="gdp_per_capita",
                 out_path="outputs/gdp_vs_internet_users.png")

    scatter_plot(df, x="life_expectancy", y="gdp_per_capita",
                 out_path="outputs/gdp_vs_life_expectancy.png")

    scatter_plot(df, x="fertility", y="gdp_per_capita",
                 out_path="outputs/gdp_vs_fertility.png")

    print("📊 Visualizations created in outputs/")


if __name__ == "__main__":
    df = pd.read_csv("data/clean_country_data.csv")
    visualize_all(df)
