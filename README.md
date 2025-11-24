# Wealth of Nations – Economic and Social Indicators Across Countries

Global economic inequality remains one of the most striking features of the modern world. As of 2025, high-income regions such as Europe and North America exhibit average GDP per capita levels often exceeding \$45,000–\$60,000, while many African nations remain below \$5,000, highlighting a disparity where wealthier regions generate nearly ten times more income per person than low-income regions. This global pattern is reflected closely within this  dataset: Europe shows an average GDP per capita of about \$47,500, North America around \$50,000, while Africa averages roughly \$6,200. These stark differences underscore the importance of understanding the social and demographic factors that accompany economic development.

This project uses a cross-sectional dataset from  of countries to study how **social indicators** such as life expectancy, internet access, fertility, unemployment, and urban population growth relate to **economic performance** measured by GDP per capita. In addition to multiple regression, the project also applies **K-means clustering** to group countries into different “development profiles” based on GDP per capita, life expectancy, internet users, fertility, and unemployment, revealing patterns such as high-income digital economies, low-income high-fertility economies, and intermediate transition economies.


---

## 1. Dataset

- **Source**: KAGGLE https://www.kaggle.com/datasets/arslaan5/global-data-gdp-life-expectancy-and-more (cross-section of countries).
- **Unit of observation**: Country.
- **Type**: Cross-sectional (one observation per country).

Key variables used in the analysis:

- **Economic**
  - `gdp`: Total GDP.
  - `gdp_per_capita`: GDP per person (main target variable).
- **Demographic / social**
  - `population`: Total population.
  - `life_expectancy_male`, `life_expectancy_female`
  - `life_expectancy`: Average of male and female life expectancy (constructed in `clean_data.py`).
  - `fertility`: Average number of children per woman.
- **Development / access**
  - `internet_users`: % of population using the internet.
  - `unemployment`: Unemployment rate (%).
  - `urban_population_growth`: Annual % growth of the urban population.
  - `secondary_school_enrollment_female`, `secondary_school_enrollment_male`
- **Meta**
  - `name`: Country name.
  - `iso2`: Two-letter ISO country code.
  - `region`: World Bank–style region (e.g. “Southern Asia”, “Western Europe”).
  - `continent`: Aggregated region (Africa, Asia, Europe, North America, South America, Oceania), created in `continent_mapping.py`.
  - `co2_emissions`, `refugees`: Additional contextual indicators.

The original raw file is stored as:

- `data/country_data.csv`

The cleaned, analysis-ready file is:

- `data/clean_country_data.csv`

---

## 2. Project Structure


```text
Wealth-of-nations/
├── data/
│   ├── country_data.csv              # Raw dataset
│   └── clean_country_data.csv        # Cleaned dataset (created by clean_data.py)
├── outputs/                          # All figures and derived CSVs
│   ├── clustered_countries.csv
│   ├── clusters_scatter.png
│   ├── continent_gdp_bar.png
│   ├── continent_heatmap.png
│   ├── gdp_vs_fertility.png
│   ├── gdp_vs_fertility_continents.png
│   ├── gdp_vs_internet_users.png
│   ├── gdp_vs_internet_users_continents.png
│   ├── gdp_vs_life_expectancy.png
│   ├── gdp_vs_life_expectancy_continents.png
│   ├── regression_coefficients_by_continent.csv
│   └── regression_continent_heatmap.png
├── scripts/
│   ├── clean_data.py                 # Cleaning + creation of life_expectancy & continent
│   ├── clustering.py                 # K-means clustering analysis
│   ├── continent_mapping.py          # Region → continent mapping helper
│   ├── regression.py                 # Global multiple regression
│   ├── regression_continents.py      # Regression by continent + heatmap of coefficients
│   ├── visualize.py                  # Simple overall scatterplots
│   └── visuals/
│       ├── visual_continents.py      # Visuals aggregated by continent
│       ├── visual_heatmaps.py        # Correlation heatmaps
│       └── visual_scatter.py         # GDP vs single indicators
├── app.py                            # Streamlit app (dashboard)
├── main.py                           # Entry script: loads cleaned data, prints summary + correlations
├── requirements.txt                  
├── .gitignore                        
└── README.md
<<<<<<< HEAD


3. Methods and Analysis
3.1 Data Cleaning (scripts/clean_data.py)

Main steps:

Load data/country_data.csv

Create combined life_expectancy

Keep essential economic & social variables

Map regions → continents

Drop missing GDP/life expectancy rows

Save cleaned file as data/clean_country_data.csv                         
=======
```  
>>>>>>> 27ee2f0 (Update README format)



## Methods and Analysis

### 3.1 Data Cleaning (scripts/clean_data.py)

Main steps performed during cleaning:

- Load the raw data from data/country_data.csv.
- Construct a combined life_expectancy variable as the mean of male and female values.
- Keep a focused subset of economic and social indicators.
- Aggregate detailed regions into broad continent categories using continent_mapping.py.
- Drop countries missing key variables (gdp_per_capita, life_expectancy).
- Save the cleaned dataset as data/clean_country_data.csv.

Run the script:


`python3 scripts/clean_data.py`





### 3.2 Exploratory Analysis (main.py and visualization scripts)

Summary Statistics (main.py)

Loads `data/clean_country_data.csv`

Prints:

Shape of the dataset

Column names

First five rows

Computes correlations between GDP per capita and:

life_expectancy

fertility

internet_users

unemployment

urban_population_growth

Run:

`python3 main.py`

Scatterplots `(scripts/visualize.py and scripts/visuals/*.py)`

Generated figures include:

GDP vs life expectancy

GDP vs internet users

GDP vs fertility

Each scatterplot is also generated by continent, producing:

`gdp_vs_life_expectancy_continents.png`

`gdp_vs_internet_users_continents.png`

`gdp_vs_fertility_continents.png`

Continental summary plots `(visual_continents.py)`:

Bar plot of average GDP per capita by continent → continent_gdp_bar.png

Continental correlation heatmap → continent_heatmap.png

These visualizations illustrate that:

Higher life expectancy is strongly associated with higher GDP per capita.

Internet usage shows one of the strongest positive relationships with income.

High fertility is strongly associated with lower GDP per capita.

Europe and North America exhibit much higher income levels than Africa and parts of Asia.

### 3.3 Multiple Regression Analysis
Global Regression `(scripts/regression.py)`

Model:

Dependent variable:
gdp_per_capita

Predictors:

life_expectancy

internet_users

fertility

unemployment

urban_population_growth

Run:

`python3 scripts/regression.py`


Key Findings (Global):

Model explains ~54% of the variation in GDP per capita (R² ≈ 0.54).

Life expectancy and internet users have strong, statistically significant positive effects.

Fertility has a strong negative relationship with GDP per capita.

Unemployment and urban population growth have weaker explanatory power.

This suggests that health outcomes and digital connectivity are major predictors of economic prosperity.

Continental Regression `(scripts/regression_continents.py)`

This script estimates the same model separately for each continent, creating:

regression_coefficients_by_continent.csv

regression_continent_heatmap.png

Run:

`python3 scripts/regression_continents.py`


Patterns by Continent:

Europe: Strong positive effects of life expectancy and internet usage.

Asia: Internet users remains a key predictor; mixed effects for fertility/unemployment.

Africa: Much lower explanatory power—suggesting unmodeled factors like institutions, infrastructure, conflict.

South America & Oceania: Mixed results but generally similar trends to the global model.

Continental models reveal that global relationships do not apply equally everywhere.

### 3.4 K-Means Clustering (scripts/clustering.py)

Clustering variables:

gdp_per_capita

life_expectancy

internet_users

fertility

unemployment

Run:

`python3 scripts/clustering.py`


Outputs:

clustered_countries.csv — each country labeled with a cluster

clusters_scatter.png — scatterplot of GDP per capita vs life expectancy with cluster colors

Cluster Interpretation :

Cluster	Characteristics	Interpretation
3	High GDP (~$47k), high life expectancy (~81), high internet (~89%), low fertility	High-income digital economies
2	Low GDP (~$1.6k), low life expectancy (~63), high fertility (~4.6), low internet (~18%)	Low-income, high-fertility economies
1	Mid-level GDP (~$7.9k), moderate social indicators	Transition economies
0	Mid-low GDP (~$6.2k), moderate internet and fertility	Developing economies

Clustering complements regression by uncovering development archetypes.

## 4. Python Libraries

The analysis uses standard scientific Python libraries:

pandas – data loading, cleaning, grouping, correlations

NumPy / SciPy – numerical operations

statsmodels – OLS regression & statistical inference

scikit-learn – K-means clustering & feature scaling

matplotlib – all visualizations

Together, these provide the computational foundation for the project.

## 5. Interactive Web Application 

In addition to the statistical and machine-learning analysis, the project includes a Streamlit web application (app.py) that makes the dataset fully interactive. 

The app provides the following features:

Interactive filtering: Select one continent or view all countries.

Country lookup tool: Search for a specific country and display its key indicators.

Variable comparison: Choose any social or demographic indicator and compare it against GDP per capita using interactive scatterplots.

Trendline toggle: Optionally add a regression line to visualize the relationship strength.

Continent comparison panel: View bar charts of average GDP per capita across continents.

Data snapshot: Displays filtered tables and summary statistics.

### How to run the dashboard
 1. Activate your virtual environment
source venv/bin/activate

 2. Install required packages (if needed)
pip install -r requirements.txt

3. Launch the Streamlit app
streamlit run app.py


Once launched, the app will automatically open in your browser:

http://localhost:8501


You can navigate through the dropdown menus and plots to interact with the dataset in real time

## 6. How to Reproduce This Project
Step 1 — Clone the Repository
git clone https://github.com/Rhodine543/Wealth-of-nations.git
cd Wealth-of-nations

Step 2 —  Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate

Step 3 — Install Dependencies
pip install -r requirements.txt

Step 4 — Clean the Data
python3 scripts/clean_data.py

Step 5 — Run Summary Analysis
python3 main.py

Step 6 — Generate Visualizations
python3 scripts/visualize.py
python3 scripts/visuals/visual_scatter.py
python3 scripts/visuals/visual_heatmaps.py
python3 scripts/visuals/visual_continents.py


Step 7 — Regression Models
python3 scripts/regression.py
python3 scripts/regression_continents.py

Step 8 — K-Means Clustering
python3 scripts/clustering.py


All outputs appear in the outputs/ folder.

## 7. Conclusively,

Countries with higher life expectancy and greater internet access enjoy significantly higher GDP per capita.

Higher fertility strongly correlates with lower income levels.

The strength and direction of these relationships vary significantly by continent.

K-means clustering reveals clear global development groups:

high-income digital economies

low-income high-fertility economies

intermediate transition economies

The combination of:

visualization

regression

unsupervised clustering
provides a rich, multi-dimensional understanding of global inequality.

