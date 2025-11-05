import streamlit as st
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/onecall"

st.set_page_config(page_title="7-Day Weather Forecast", page_icon="🌤️", layout="centered")
st.title("🌦️ 7-Day Weather Forecast")
st.write("Powered by [OpenWeatherMap](https://openweathermap.org/).")

city = st.text_input("Enter city name:", placeholder="e.g. Paris, London, Tokyo")

def get_coordinates(city_name):
    params = {"q": city_name, "appid": API_KEY}
    res = requests.get(WEATHER_URL, params=params)
    if res.status_code == 200:
        data = res.json()
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        return lat, lon, data
    else:
        return None, None, None

def get_forecast(lat, lon):
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "minutely,hourly,alerts",
        "units": "metric",
        "appid": API_KEY
    }
    res = requests.get(FORECAST_URL, params=params)
    if res.status_code == 200:
        return res.json()
    else:
        st.error(f"Error {res.status_code}: {res.text}")
        return None

if city:
    lat, lon, current_data = get_coordinates(city)
    if lat and lon:
        forecast_data = get_forecast(lat, lon)
        if forecast_data:
            current_weather = current_data["weather"][0]
            temp = current_data["main"]["temp"]
            desc = current_weather["description"].capitalize()
            icon = current_weather["icon"]

            st.subheader(f"Current weather in {city.title()}")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")
            with col2:
                st.markdown(f"**{desc}**")
                st.metric("🌡️ Temperature", f"{temp:.1f} °C")

            st.divider()
            st.subheader("📅 7-Day Forecast")

            daily = forecast_data["daily"]
            for day in daily[:7]:
                date = datetime.fromtimestamp(day["dt"]).strftime("%A, %b %d")
                min_temp = day["temp"]["min"]
                max_temp = day["temp"]["max"]
                weather_desc = day["weather"][0]["description"].capitalize()
                icon = day["weather"][0]["icon"]

                with st.container():
                    col1, col2, col3 = st.columns([1, 4, 2])
                    col1.image(f"http://openweathermap.org/img/wn/{icon}.png", width=60)
                    col2.markdown(f"**{date}**")
                    col2.caption(weather_desc)
                    col3.metric("Temp (min/max)", f"{min_temp:.1f}°C / {max_temp:.1f}°C")
                    st.markdown("---")
        else:
            st.error("Failed to fetch forecast data.")
    else:
        st.error("City not found. Please try again.")
