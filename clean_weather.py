import pandas as pd

file_path = "../data/weather_data.csv"

df = pd.read_csv(file_path)

print("Before Cleaning")
print("================")
print(df)

# Remove duplicate records
df = df.drop_duplicates()

# Remove rows with missing values
df = df.dropna()

# Save cleaned data
df.to_csv("../data/cleaned_weather_data.csv", index=False)

print("\nAfter Cleaning")
print("===============")
print(df)

print("\nCleaned data saved successfully!")