import time
import csv
import os

from weather_api import get_weather


file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "weather_data.csv")


def save_weather(weather):

    file_exists = os.path.exists(file_path)

    with open(file_path, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "time",
                "temperature",
                "humidity",
                "wind_speed"
            ])

        writer.writerow([
            weather["time"],
            weather["temperature"],
            weather["humidity"],
            weather["wind_speed"]
        ])


print("Weather Streaming Started")
print("=========================")

while True:

    weather = get_weather()

    if weather:

        save_weather(weather)

        print("\nNew Weather Record")
        print("-------------------")
        print("Time:", weather["time"])
        print("Temperature:", weather["temperature"], "°C")
        print("Humidity:", weather["humidity"], "%")
        print("Wind Speed:", weather["wind_speed"], "km/h")
        print("Data saved to CSV")

    else:
        print("Weather data not received")

    time.sleep(60)