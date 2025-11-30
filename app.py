import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Wealth of Nations Dashboard", layout="wide")


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


# Title + header message
st.title("🌍 Wealth of Nations – Interactive Dashboard")

st.markdown(
    """
This dashboard allows you to explore how **economic performance** (GDP per capita)  
relates to **social indicators** such as life expectancy, fertility, internet usage,  
and other demographic characteristics.  

Use the sidebar to filter by continent, compare variables, search for countries,  
and visualize patterns in the global data.
"""
)

# ---------- SIDEBAR ----------
st.sidebar.header("Controls")

# Continent filter
selected_continent = st.sidebar.selectbox(
    "Select continent (or All):",
    options=["All"] + continents,
)

# Variable for main scatterplot
target_var = "gdp_per_capita"
x_var = st.sidebar.selectbox(
    "Compare GDP per capita against:",
    options=[c for c in numeric_cols if c != target_var],
    index=1,
)

show_trendline = st.sidebar.checkbox("Show regression line", value=True)

# Country search tool
st.sidebar.markdown("---")
st.sidebar.subheader("Country search")

country_query = st.sidebar.text_input(
    "Search country (name or ISO2):",
    value="",
    placeholder="e.g. France or FR",
)

# ---------- FILTERED DATA ----------
if selected_continent != "All":
    df_view = df[df["continent"] == selected_continent].copy()
else:
    df_view = df.copy()

# ---------- COUNTRY SEARCH RESULT ----------
if country_query.strip():
    q = country_query.strip().lower()
    country_match = df[
        (df["name"].str.lower().str.contains(q))
        | (df["iso2"].str.lower() == q)
    ]

    st.subheader("Country search result")

    if country_match.empty:
        st.write("No country found matching that query.")
    else:
        display_cols = [
            "name",
            "iso2",
            "continent",
            "region",
            "gdp_per_capita",
            "life_expectancy",
            "internet_users",
            "fertility",
            "unemployment",
        ]
        display_cols = [c for c in display_cols if c in country_match.columns]
        st.dataframe(country_match[display_cols])

        # Metrics row if single match
        if len(country_match) == 1:
            row = country_match.iloc[0]
            c1, c2, c3 = st.columns(3)
            if "gdp_per_capita" in row:
                c1.metric("GDP per capita", f"{row['gdp_per_capita']:,.0f}")
            if "life_expectancy" in row:
                c2.metric("Life expectancy", f"{row['life_expectancy']:.1f} years")
            if "internet_users" in row:
                c3.metric("Internet users", f"{row['internet_users']:.1f}%")

# ---------- DATA SNAPSHOT ----------
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

# ---------- CONTINENT COMPARISON DASHBOARD ----------
st.subheader("Continent comparison dashboard")

comparison_vars = [
    "gdp_per_capita",
    "life_expectancy",
    "internet_users",
    "fertility",
    "unemployment",
]

indicator = st.selectbox(
    "Choose indicator to compare across continents:",
    options=comparison_vars,
    index=0,
    format_func=lambda c: c.replace("_", " ").title(),
)

continent_summary = (
    df.groupby("continent")[comparison_vars]
    .mean()
    .round(2)
    .sort_values("gdp_per_capita", ascending=False)
)

st.write("Average values by continent:")
st.dataframe(continent_summary)

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.barplot(
    x=continent_summary.index,
    y=continent_summary[indicator],
    ax=ax2,
)
ax2.set_ylabel(indicator.replace("_", " ").title())
ax2.set_xlabel("Continent")
ax2.set_title(f"Average {indicator.replace('_', ' ').title()} by continent")
plt.xticks(rotation=30)
st.pyplot(fig2)
