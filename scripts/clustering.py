"""
K-Means Clustering on Country Development Indicators

Clusters countries based on:
- GDP per capita
- Life expectancy
- Internet users
- Fertility
- Unemployment

Outputs:
- outputs/clusters_scatter.png
- outputs/clustered_countries.csv
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path("data/clean_country_data.csv")
OUT_PATH_CSV = Path("outputs/clustered_countries.csv")
OUT_PATH_PLOT = Path("outputs/clusters_scatter.png")

def main():

    # -------------------------------
    # 1. Load cleaned dataset
    # -------------------------------
    df = pd.read_csv(DATA_PATH)

    # Variables to cluster on
    features = [
        "gdp_per_capita",
        "life_expectancy",
        "internet_users",
        "fertility",
        "unemployment",
    ]

    # Drop missing values for clustering
    df_cluster = df.dropna(subset=features).copy()

    # -------------------------------
    # 2. Standardize 
    # -------------------------------
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_cluster[features])

    # -------------------------------
    # 3. Run K-Means clustering
    # -------------------------------
    k = 4   # number of clusters
    kmeans = KMeans(n_clusters=k, random_state=42)
    df_cluster["cluster"] = kmeans.fit_predict(X_scaled)

    # -------------------------------
    # 4. Save clustered data
    # -------------------------------
    OUT_PATH_CSV.parent.mkdir(exist_ok=True, parents=True)
    df_cluster.to_csv(OUT_PATH_CSV, index=False)
    print(f"✔ Saved clustered dataset to {OUT_PATH_CSV}")

    # -------------------------------
    # 5. Visualize clusters
    # Scatter: GDP per capita vs Life expectancy
    # -------------------------------
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df_cluster,
        x="life_expectancy",
        y="gdp_per_capita",
        hue="cluster",
        palette="tab10",
        s=100
    )

    for _, row in df_cluster.iterrows():
        plt.text(row["life_expectancy"], row["gdp_per_capita"], row["iso2"], fontsize=7)

    plt.title("K-Means Clusters of Countries")
    plt.xlabel("Life Expectancy")
    plt.ylabel("GDP per Capita")
    plt.tight_layout()

    plt.savefig(OUT_PATH_PLOT)
    print(f"✔ Saved cluster scatterplot to {OUT_PATH_PLOT}")

    # -------------------------------
    # 6. Describe cluster characteristics
    # -------------------------------
    print("\n📌 Cluster Summary (mean values):")
    print(df_cluster.groupby("cluster")[features].mean())


if __name__ == "__main__":
    main()
