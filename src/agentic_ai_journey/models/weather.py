from pydantic import BaseModel, Field

class Location(BaseModel):
    name: str
    country: str | None = None
    latitude: float
    longitude: float

class CurrentWeather(BaseModel):
    temperature: float = Field(alias="temperature_2m", description="Temperature in °C")
    wind_speed: float = Field(alias="wind_speed_10m", description="Wind speed in km/h")

class WeatherReport(BaseModel):
    location: Location
    weather: CurrentWeather
