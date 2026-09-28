import requests


def get_weather():

    latitude = 11.3410
    longitude = 77.7172

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        current = data["current"]

        weather = {
            "time": current["time"],
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"]
        }

        return weather

    else:
        print("API request failed")
        return None


if __name__ == "__main__":

    weather = get_weather()

    if weather:
        print("Weather Data")
        print("----------------")
        print("Time:", weather["time"])
        print("Temperature:", weather["temperature"], "°C")
        print("Humidity:", weather["humidity"], "%")
        print("Wind Speed:", weather["wind_speed"], "km/h")