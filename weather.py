import requests
from config import API_KEY, UNITS

def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={UNITS}"
        response = requests.get(url)
        data = response.json()

        weather = {
            "city": city,
            "condition": data["weather"][0]["main"],
            "weather_icon": data["weather"][0]["icon"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "solar_radiation": estimate_solar_radiation(data["clouds"]["all"])
        }
        return weather
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return {
            "city": city,
            "condition": "Unknown",
            "weather_icon": "01d",
            "temperature": 0,
            "humidity": 0,
            "wind_speed": 0,
            "solar_radiation": 0
        }

def estimate_solar_radiation(cloud_coverage):
    return round((100 - cloud_coverage) * 10, 2)
