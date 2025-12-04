import requests
import os

API_KEY = os.getenv("WEATHER_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city: "Merida"): # type: ignore (dijo copilot)
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "es"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code != 200:
            return "No pude obtener el clima."
        
        data = response.json()

        description = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
    
        return f"{description}, {temp}°C (se siente como {feels}°C)."
    
    except:
        return "Error de conexión al obtener el clima."
        