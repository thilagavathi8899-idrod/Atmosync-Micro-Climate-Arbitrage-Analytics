import pandas as pd

file_path = "../data/weather_data.csv"

df = pd.read_csv(file_path)

print("Weather Data Analysis")
print("=====================")

print("\nNumber of Records:", len(df))

print("\nAverage Temperature:", df["temperature"].mean(), "°C")

print("Average Humidity:", df["humidity"].mean(), "%")

print("Average Wind Speed:", df["wind_speed"].mean(), "km/h")

print("\nMissing Values:")
print(df.isnull().sum())

print("\nWeather Data:")
print(df)