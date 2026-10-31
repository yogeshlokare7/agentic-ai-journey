import os
from types import TracebackType

import httpx

from agentic_ai_journey.models.weather import CurrentWeather, Location, WeatherReport


class CityNotFoundError(Exception):
    def __init__(self, city: str) -> None:
        super().__init__(f"City {city!r} not found")
        self.city = city


class WeatherClient:
    def __init__(
        self,
        geocoding_url: str | None = None,
        forecast_url: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        geocoding_url = geocoding_url or os.getenv("GEOCODING_BASE_URL")
        forecast_url = forecast_url or os.getenv("FORECAST_BASE_URL")
        if not geocoding_url or not forecast_url:
            raise ValueError(
                "GEOCODING_BASE_URL and FORECAST_BASE_URL must be set in the environment or .env file"
            )
        self._geocoding = httpx.AsyncClient(base_url=geocoding_url, timeout=timeout)
        self._forecast = httpx.AsyncClient(base_url=forecast_url, timeout=timeout)

    async def geocode(self, city: str) -> Location:
        response = await self._geocoding.get("/search", params={"name": city, "count": 1})
        response.raise_for_status()
        # The API omits "results" entirely when nothing matches.
        results = response.json().get("results")
        if not results:
            raise CityNotFoundError(city)
        return Location.model_validate(results[0])

    async def current_weather(self, location: Location) -> CurrentWeather:
        response = await self._forecast.get(
            "/forecast",
            params={
                "latitude": location.latitude,
                "longitude": location.longitude,
                "current": "temperature_2m,wind_speed_10m",
                "temperature_unit": "celsius",
                "wind_speed_unit": "kmh",
            },
        )
        response.raise_for_status()
        return CurrentWeather.model_validate(response.json()["current"])

    async def report(self, city: str) -> WeatherReport:
        location = await self.geocode(city)
        weather = await self.current_weather(location)
        return WeatherReport(location=location, weather=weather)

    async def aclose(self) -> None:
        await self._geocoding.aclose()
        await self._forecast.aclose()

    async def __aenter__(self) -> "WeatherClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()
