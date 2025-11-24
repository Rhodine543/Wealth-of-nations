import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean_country_data.csv")

variables = [
    "life_expectancy",
    "internet_users",
    "fertility",
    "unemployment",
    "urban_population_growth",
]

results = []

# Run regression for each continent
for continent, sub in df.groupby("continent"):
    sub_clean = sub[variables + ["gdp_per_capita"]].dropna()

    if len(sub_clean) < 10:
        print(f"⏩ Skipping {continent}: not enough data.")
        continue

    X = sub_clean[variables]
    X = sm.add_constant(X)   # add intercept
    y = sub_clean["gdp_per_capita"]

    model = sm.OLS(y, X).fit()

    coef_df = model.params.to_frame(name=continent)
    results.append(coef_df)

    print(f"\n📌 Regression results for {continent}")
    print(model.summary())

# Combine coefficients into one table
coef_table = pd.concat(results, axis=1)
coef_table.to_csv("outputs/regression_coefficients_by_continent.csv")
print("\n✔️ Saved: outputs/regression_coefficients_by_continent.csv")


