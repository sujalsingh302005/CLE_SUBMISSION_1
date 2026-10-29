"""Week 2 Tasks 3-4. Pulls NYC hourly weather from the free Open-Meteo API (no key needed).
Run: python -m taxi_pipeline.pull_api"""
from taxi_pipeline.api_client import APIError, fetch_and_save

URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {"latitude": 40.71, "longitude": -74.01, "hourly": "temperature_2m,precipitation"}

if __name__ == "__main__":
    try:
        fetch_and_save(URL, "data/raw/api_response.json", params=PARAMS)
    except APIError as exc:
        raise SystemExit(f"API pull failed: {exc}") from exc
