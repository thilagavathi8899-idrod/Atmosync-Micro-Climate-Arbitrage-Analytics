
# ============================================================
# ATMOSYNC: MICRO-CLIMATE ARBITRAGE ANALYTICS
# Internship Project - Infotact Solutions
# Intern: Rajesh Devda
# Domain: Data Analytics
# ============================================================

# STEP 1: IMPORT LIBRARIES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

print("=" * 60)
print("ATMOSYNC: MICRO-CLIMATE ARBITRAGE ANALYTICS")
print("Infotact Solutions | Data Associate L1 Intern")
print("=" * 60)

# STEP 2: CREATE PROJECT FOLDERS

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
CHART_DIR = BASE_DIR / "outputs" / "charts"
RESULT_DIR = BASE_DIR / "outputs" / "results"

for folder in [RAW_DIR, PROCESSED_DIR, CHART_DIR, RESULT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

print("\nProject folders created successfully!")

# STEP 3: GENERATE PRACTICE WEATHER DATASET
# Note: This is synthetic data, not actual weather observations.

np.random.seed(42)

locations = {
    "Pune": {"temp": 25, "humidity": 60},
    "Mumbai": {"temp": 29, "humidity": 75},
    "Nashik": {"temp": 23, "humidity": 55},
    "Bengaluru": {"temp": 24, "humidity": 68},
    "Delhi": {"temp": 22, "humidity": 58},
    "Hyderabad": {"temp": 27, "humidity": 62}
}

dates = pd.date_range("2026-01-01", "2026-03-31", freq="D")

records = []

for date in dates:
    seasonal_change = 2 * np.sin(
        2 * np.pi * date.dayofyear / 365
    )

    for location, values in locations.items():
        temperature = (
            values["temp"]
            + seasonal_change
            + np.random.normal(0, 2.5)
        )

        humidity = (
            values["humidity"]
            + np.random.normal(0, 5)
        )

        rainfall = max(0, np.random.exponential(2))

        wind_speed = max(0, np.random.normal(10, 3))

        pressure = np.random.normal(1012, 5)

        weather_condition = (
            "Rainy" if rainfall > 5
            else "Cloudy" if humidity > 75
            else "Sunny"
        )

        records.append([
            date,
            location,
            temperature,
            humidity,
            rainfall,
            wind_speed,
            pressure,
            weather_condition
        ])

df = pd.DataFrame(records, columns=[
    "Date",
    "Location",
    "Temperature",
    "Humidity",
    "Rainfall",
    "Wind_Speed",
    "Pressure",
    "Weather_Condition"
])

df.to_csv(RAW_DIR / "weather_raw.csv", index=False)

print("\nSTEP 1: DATASET CREATED")
print("Total Records:", len(df))
print("Total Locations:", df["Location"].nunique())
print("Dataset saved in data/raw/")

# STEP 4: DATASET OVERVIEW

print("\nSTEP 2: DATASET OVERVIEW")

print("\nFirst 5 Records:")
print(df.head().to_string(index=False))

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe().round(2))

# STEP 5: DATA VALIDATION AND CLEANING

print("\nSTEP 3: DATA CLEANING")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:", df.duplicated().sum())

df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates().copy()

numeric_columns = [
    "Temperature",
    "Humidity",
    "Rainfall",
    "Wind_Speed",
    "Pressure"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")
    df[column] = df[column].fillna(df[column].median())

df["Humidity"] = df["Humidity"].clip(0, 100)
df["Rainfall"] = df["Rainfall"].clip(lower=0)
df["Wind_Speed"] = df["Wind_Speed"].clip(lower=0)

df = df.dropna(subset=["Date", "Location"])

df.to_csv(PROCESSED_DIR / "weather_cleaned.csv", index=False)

print("Data cleaning completed successfully!")
print("Cleaned dataset:", df.shape)

# STEP 6: EXPLORATORY DATA ANALYSIS

print("\nSTEP 4: EXPLORATORY DATA ANALYSIS")

location_summary = df.groupby("Location").agg(
    Average_Temperature=("Temperature", "mean"),
    Average_Humidity=("Humidity", "mean"),
    Total_Rainfall=("Rainfall", "sum"),
    Average_Wind_Speed=("Wind_Speed", "mean"),
    Average_Pressure=("Pressure", "mean")
).round(2)

print("\nLocation-wise Analysis:")
print(location_summary)

location_summary.to_csv(RESULT_DIR / "location_summary.csv")

print("\nOverall Average Temperature:",
      round(df["Temperature"].mean(), 2), "°C")

print("Overall Average Humidity:",
      round(df["Humidity"].mean(), 2), "%")

print("Overall Total Rainfall:",
      round(df["Rainfall"].sum(), 2), "mm")

print("Overall Average Wind Speed:",
      round(df["Wind_Speed"].mean(), 2))

# STEP 7: TEMPERATURE COMPARISON

plt.figure(figsize=(10, 6))

sns.barplot(
    data=df,
    x="Location",
    y="Temperature",
    estimator=np.mean
)

plt.title("Average Temperature by Location")
plt.xlabel("Location")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "temperature_comparison.png", dpi=300)
plt.show()

# STEP 8: HUMIDITY COMPARISON

plt.figure(figsize=(10, 6))

sns.barplot(
    data=df,
    x="Location",
    y="Humidity",
    estimator=np.mean
)

plt.title("Average Humidity by Location")
plt.xlabel("Location")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "humidity_comparison.png", dpi=300)
plt.show()

# STEP 9: RAINFALL COMPARISON

plt.figure(figsize=(10, 6))

sns.barplot(
    data=df,
    x="Location",
    y="Rainfall",
    estimator=np.sum
)

plt.title("Total Rainfall by Location")
plt.xlabel("Location")
plt.ylabel("Rainfall (mm)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "rainfall_comparison.png", dpi=300)
plt.show()

# STEP 10: DAILY TEMPERATURE TREND

daily_temperature = df.groupby("Date")["Temperature"].mean()

plt.figure(figsize=(12, 6))
plt.plot(daily_temperature.index, daily_temperature.values)
plt.title("Daily Average Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "temperature_trend.png", dpi=300)
plt.show()

# STEP 11: DAILY HUMIDITY TREND

daily_humidity = df.groupby("Date")["Humidity"].mean()

plt.figure(figsize=(12, 6))
plt.plot(daily_humidity.index, daily_humidity.values)
plt.title("Daily Average Humidity Trend")
plt.xlabel("Date")
plt.ylabel("Humidity (%)")
plt.grid(True)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "humidity_trend.png", dpi=300)
plt.show()

# STEP 12: RAINFALL TREND

daily_rainfall = df.groupby("Date")["Rainfall"].sum()

plt.figure(figsize=(12, 6))
plt.plot(daily_rainfall.index, daily_rainfall.values)
plt.title("Daily Rainfall Trend")
plt.xlabel("Date")
plt.ylabel("Rainfall (mm)")
plt.grid(True)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "rainfall_trend.png", dpi=300)
plt.show()

# STEP 13: TEMPERATURE VS HUMIDITY

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="Temperature",
    y="Humidity",
    hue="Location"
)

plt.title("Temperature vs Humidity")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.savefig(CHART_DIR / "temperature_vs_humidity.png", dpi=300)
plt.show()

# STEP 14: CORRELATION HEATMAP

correlation = df[numeric_columns].corr()

plt.figure(figsize=(9, 7))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Weather Variables Correlation")
plt.tight_layout()
plt.savefig(CHART_DIR / "correlation_heatmap.png", dpi=300)
plt.show()

# STEP 15: MICRO-CLIMATE DIFFERENCE SCORE
# The score measures how distinct each location's
# average weather profile is from the other locations.
# It is not a financial arbitrage or trading signal.

print("\nSTEP 5: MICRO-CLIMATE ANALYSIS")

features = [
    "Temperature",
    "Humidity",
    "Rainfall",
    "Wind_Speed",
    "Pressure"
]

climate_data = df.groupby("Location")[features].mean()

scaler = MinMaxScaler()
scaled_values = scaler.fit_transform(climate_data)

scaled_df = pd.DataFrame(
    scaled_values,
    columns=features,
    index=climate_data.index
)

# Pairwise Euclidean distance between locations.
distance_matrix = np.zeros(
    (len(scaled_df), len(scaled_df))
)

for i in range(len(scaled_df)):
    for j in range(len(scaled_df)):
        distance_matrix[i, j] = np.sqrt(
            np.sum((scaled_values[i] - scaled_values[j]) ** 2)
        )

# Average distance from all other locations.
n_locations = len(scaled_df)

climate_scores = (
    distance_matrix.sum(axis=1) / (n_locations - 1)
)

score_df = pd.DataFrame({
    "Location": scaled_df.index,
    "MicroClimate_Score": climate_scores
})

score_df = score_df.sort_values(
    "MicroClimate_Score",
    ascending=False
).reset_index(drop=True)

print("\nMicro-Climate Difference Scores:")
print(score_df.round(3).to_string(index=False))

score_df.to_csv(
    RESULT_DIR / "microclimate_scores.csv",
    index=False
)

# STEP 16: MICRO-CLIMATE SCORE CHART

plt.figure(figsize=(10, 6))

sns.barplot(
    data=score_df,
    x="Location",
    y="MicroClimate_Score"
)

plt.title("Micro-Climate Difference Score by Location")
plt.xlabel("Location")
plt.ylabel("Average Normalized Distance")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(CHART_DIR / "microclimate_score.png", dpi=300)
plt.show()

# STEP 17: LOCATION-WISE TEMPERATURE AND HUMIDITY

monthly_data = df.copy()
monthly_data["Month"] = monthly_data["Date"].dt.to_period("M").astype(str)

monthly_summary = monthly_data.groupby(
    ["Month", "Location"]
).agg(
    Average_Temperature=("Temperature", "mean"),
    Average_Humidity=("Humidity", "mean"),
    Total_Rainfall=("Rainfall", "sum")
).reset_index().round(2)

monthly_summary.to_csv(
    RESULT_DIR / "monthly_analysis.csv",
    index=False
)

print("\nMonthly analysis saved successfully!")

# STEP 18: AUTOMATIC INSIGHTS

print("\n" + "=" * 60)
print("ATMOSYNC: AUTOMATIC PROJECT INSIGHTS")
print("=" * 60)

highest_temp = location_summary["Average_Temperature"].idxmax()
lowest_temp = location_summary["Average_Temperature"].idxmin()
highest_humidity = location_summary["Average_Humidity"].idxmax()
highest_rainfall = location_summary["Total_Rainfall"].idxmax()
highest_score = score_df.iloc[0]["Location"]

insights = [
    f"Highest average temperature: {highest_temp}",
    f"Lowest average temperature: {lowest_temp}",
    f"Highest average humidity: {highest_humidity}",
    f"Highest total rainfall: {highest_rainfall}",
    f"Most distinct average climate profile: {highest_score}",
    f"Overall average temperature: {df['Temperature'].mean():.2f} °C",
    f"Overall average humidity: {df['Humidity'].mean():.2f}%",
    f"Total recorded rainfall in dataset: {df['Rainfall'].sum():.2f} mm"
]

for number, insight in enumerate(insights, start=1):
    print(f"{number}. {insight}")

with open(RESULT_DIR / "project_insights.txt", "w", encoding="utf-8") as file:
    file.write("ATMOSYNC PROJECT INSIGHTS\n\n")
    for number, insight in enumerate(insights, start=1):
        file.write(f"{number}. {insight}\n")

# STEP 19: FINAL ANALYSIS REPORT

final_results = location_summary.reset_index().merge(
    score_df,
    on="Location"
)

final_results = final_results.round(2)

final_results.to_csv(
    RESULT_DIR / "final_analysis_results.csv",
    index=False
)

print("\nFinal Analysis Results:")
print(final_results.to_string(index=False))

# STEP 20: PROJECT COMPLETION

print("\n" + "=" * 60)
print("ATMOSYNC PROJECT COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nGenerated files:")
print("1. Raw dataset")
print("2. Cleaned dataset")
print("3. Location summary")
print("4. Monthly analysis")
print("5. Micro-climate scores")
print("6. Final analysis results")
print("7. Project insights")
print("8. 8 analytical charts")

print("\nAll files are available in the data and outputs folders.")
print("You can now use the CSV files in Power BI.")