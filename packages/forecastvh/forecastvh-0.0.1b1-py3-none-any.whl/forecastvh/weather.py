import json
import requests
from dataclasses import dataclass


@dataclass
class Podcast:
    """Forecast metadata."""

    id: int
    country: str
    city: str
    temp: int
    feels_like: int
    pressure: int
    humidity: int
    wind_speed: int
    cloudiness: int
    status: str


@dataclass
class Error:
    """Error status metadata."""

    message: str
    status: str


def get_weather(city: str, units: str = "metric", lang: str = "en"):
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&units="
        + units
        + "&appid=06c10220631ddd0737fd3903a24eda98&lang="
        + lang
        + ""
    )
    todos = json.loads(response.text)
    if todos["cod"] == 200:
        result = Podcast(
            id=todos["id"],
            country=todos["sys"]["country"],
            city=todos["name"],
            temp=todos["main"]["temp"],
            feels_like=todos["main"]["feels_like"],
            pressure=todos["main"]["pressure"],
            humidity=todos["main"]["humidity"],
            wind_speed=todos["wind"]["speed"],
            cloudiness=todos["clouds"]["all"],
            status=todos["cod"],
        )
        return result
    else:
        error = Error(status="404", message=todos["message"])
        return error
