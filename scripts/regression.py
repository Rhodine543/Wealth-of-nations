import pandas as pd
import statsmodels.api as sm


def run_regression(df: pd.DataFrame):
    """
    Runs a multiple linear regression with gdp_per_capita as the target.
    """

    # Selects predictor variables (based on the correlations)
    predictors = [
        "life_expectancy",
        "internet_users",
        "fertility",
        "unemployment",
        "urban_population_growth"
    ]

    # Drop rows with missing values in selected columns
    data = df[["gdp_per_capita"] + predictors].dropna()

    X = data[predictors]
    y = data["gdp_per_capita"]

    # Add constant for intercept
    X = sm.add_constant(X)

    # Fit model
    model = sm.OLS(y, X).fit()

    print("\n📈 MULTIPLE REGRESSION RESULTS")
    print(model.summary())

    return model


if __name__ == "__main__":
    df = pd.read_csv("data/clean_country_data.csv")
    run_regression(df)
