# 8dd4d0dab1843207038e1646bdcbb78b
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Streamlit UI setup
st.set_page_config(page_title="Weather Dashboard", page_icon="🌦️", layout="centered")

st.title("🌤️ Weather Dashboard")
st.write("Get real-time weather data powered by [OpenWeatherMap](https://openweathermap.org/).")

city = st.text_input("Enter a city name:", placeholder="e.g. London")

def get_weather(city_name):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if city:
    weather_data = get_weather(city)
    
    if weather_data:
        # Extract relevant data
        main = weather_data["main"]
        wind = weather_data["wind"]
        weather = weather_data["weather"][0]
        
        temp = main["temp"]
        feels_like = main["feels_like"]
        humidity = main["humidity"]
        wind_speed = wind["speed"]
        description = weather["description"].capitalize()
        icon = weather["icon"]
        
        # Display data
        st.subheader(f"Weather in {city.title()}")
        st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=100)
        st.markdown(f"**{description}**")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature", f"{temp} °C")
        col2.metric("🤗 Feels Like", f"{feels_like} °C")
        col3.metric("💧 Humidity", f"{humidity}%")
        
        st.metric("🌬️ Wind Speed", f"{wind_speed} m/s")
    else:
        st.error("City not found or API error. Please check your input or API key.")
