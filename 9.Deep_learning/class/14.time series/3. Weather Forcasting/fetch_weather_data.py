"""Download daily historical weather from the Open-Meteo Archive API."""

import argparse
import re
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
DAILY_VARIABLES = [
    "temperature_2m_mean",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "wind_speed_10m_max",
]


def find_location(city: str, country: str | None = None) -> dict:
    response = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 10, "language": "en", "format": "json"},
        timeout=30,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    if country:
        results = [
            item
            for item in results
            if item.get("country", "").casefold() == country.casefold()
            or item.get("country_code", "").casefold() == country.casefold()
        ]
    if not results:
        qualifier = f" in {country}" if country else ""
        raise ValueError(f"No matching location found for {city}{qualifier}.")
    return results[0]


def fetch_weather(
    city: str,
    country: str,
    start_date: date,
    end_date: date,
    output_dir: Path,
) -> Path:
    if start_date > end_date:
        raise ValueError("Start date must be on or before end date.")

    location = find_location(city, country)
    response = requests.get(
        ARCHIVE_URL,
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": ",".join(DAILY_VARIABLES),
            "timezone": "auto",
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()

    daily = payload.get("daily")
    if not daily or not daily.get("time"):
        raise ValueError("Open-Meteo returned no daily weather records.")

    data = pd.DataFrame(
        {
            "date": daily["time"],
            "temperature_mean_c": daily["temperature_2m_mean"],
            "temperature_max_c": daily["temperature_2m_max"],
            "temperature_min_c": daily["temperature_2m_min"],
            "precipitation_mm": daily["precipitation_sum"],
            "wind_speed_max_kmh": daily["wind_speed_10m_max"],
        }
    )
    data.insert(1, "city", location["name"])
    data.insert(2, "country", location.get("country", country))
    data.insert(3, "latitude", payload["latitude"])
    data.insert(4, "longitude", payload["longitude"])

    slug = re.sub(r"[^a-z0-9]+", "_", location["name"].casefold()).strip("_")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{slug}_daily_weather.csv"
    data.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", default="Mumbai", help="City to download (default: Mumbai)")
    parser.add_argument("--country", default="India", help="Country name or code")
    parser.add_argument("--start-date", type=date.fromisoformat, default=date(2015, 1, 1))
    parser.add_argument(
        "--end-date",
        type=date.fromisoformat,
        default=date.today() - timedelta(days=7),
        help="Use a complete historical date; defaults to seven days ago",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent / "data",
    )
    args = parser.parse_args()

    output_path = fetch_weather(
        city=args.city,
        country=args.country,
        start_date=args.start_date,
        end_date=args.end_date,
        output_dir=args.output_dir,
    )
    print(f"Saved real historical weather data to {output_path}")


if __name__ == "__main__":
    main()
