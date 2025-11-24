import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("data/clean_country_data.csv")

df = load_data()

# Basic prepared lists
numeric_cols = [
    "gdp_per_capita",
    "life_expectancy",
    "fertility",
    "internet_users",
    "unemployment",
    "urban_population_growth",
    "co2_emissions",
    "refugees",
]
continents = sorted(df["continent"].dropna().unique())

# ---------- PAGE LAYOUT ----------
st.set_page_config(page_title="Wealth of Nations Dashboard", layout="wide")

st.title("🌍 Wealth of Nations – Interactive Dashboard")

st.markdown(
    """
This dashboard lets you explore how **economic performance** (GDP per capita)  
relates to **social indicators** like life expectancy, fertility, internet use, and more.

Use the controls in the sidebar to filter by **continent** and choose **variables**.
"""
)

# ---------- SIDEBAR ----------
st.sidebar.header("Filters & Options")

selected_continent = st.sidebar.selectbox(
    "Select continent (or All):",
    options=["All"] + continents,
)

target_var = "gdp_per_capita"
x_var = st.sidebar.selectbox(
    "Choose a variable to compare against GDP per capita:",
    options=[c for c in numeric_cols if c != target_var],
    index=1,  # e.g. life_expectancy by default
)

show_trendline = st.sidebar.checkbox("Show regression line", value=True)

# Filter by continent if needed
if selected_continent != "All":
    df_view = df[df["continent"] == selected_continent].copy()
else:
    df_view = df.copy()

st.subheader("Dataset snapshot")

st.write(f"**Filtered rows:** {len(df_view)}")
st.dataframe(df_view[["name", "continent", "region", target_var, x_var]].head(10))

# ---------- SUMMARY STATS ----------
st.subheader("Summary statistics (filtered data)")
st.write(df_view[numeric_cols].describe())

# ---------- SCATTERPLOT ----------
st.subheader(f"GDP per capita vs. {x_var.replace('_', ' ').title()}")

fig, ax = plt.subplots(figsize=(7, 5))
sns.scatterplot(
    data=df_view,
    x=x_var,
    y=target_var,
    hue="continent",
    ax=ax,
)

if show_trendline and len(df_view) > 2:
    sns.regplot(
        data=df_view,
        x=x_var,
        y=target_var,
        scatter=False,
        ax=ax,
    )

ax.set_xlabel(x_var.replace("_", " ").title())
ax.set_ylabel("GDP per capita")
ax.set_title(f"GDP per capita vs. {x_var.replace('_', ' ').title()}")

st.pyplot(fig)

# ---------- CONTINENT BAR CHART ----------
st.subheader("Average GDP per capita by continent (for filtered data)")

gdp_by_continent = (
    df_view.groupby("continent")[target_var]
    .mean()
    .sort_values(ascending=False)
)

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.barplot(
    x=gdp_by_continent.index,
    y=gdp_by_continent.values,
    ax=ax2,
)
ax2.set_ylabel("Average GDP per capita")
ax2.set_xlabel("Continent")
ax2.set_title("Average GDP per capita by continent")
plt.xticks(rotation=30)

st.pyplot(fig2)

st.markdown(
    """
---
✅ This app is built from your project code and cleaned dataset (`data/clean_country_data.csv`).  
You can mention this dashboard in your report as your **bonus web application**.
"""
)
