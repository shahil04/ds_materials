import streamlit as st
import requests

API_KEY = "30dc3ec276c49ac523473c3cfb2848e0"

def get_lat_lon(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    res = requests.get(url).json()
    if not res:
        return None, None
    return res[0]["lat"], res[0]["lon"]

def get_current_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    return requests.get(url).json()

st.title("🌤 Today's Weather")

city = st.text_input("Enter city name", "Delhi")

if st.button("Fetch Weather"):
    lat, lon = get_lat_lon(city)
    if lat is None:
        st.error("City not found.")
    else:
        data = get_current_weather(lat, lon)

        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        col1, col2 = st.columns([1,3])

        with col1:
            st.image(icon_url, width=120)

        with col2:
            st.markdown(f"""<h2>{city}</h2>
            <h3>{data['weather'][0]['description'].title()}</h3>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        colA, colB, colC, colD = st.columns(4)
        colA.metric("🌡 Temperature", f"{data['main']['temp']} °C")
        colB.metric("💧 Humidity", f"{data['main']['humidity']} %")
        colC.metric("⚡ Pressure", f"{data['main']['pressure']} hPa")
        colD.metric("🌬 Wind Speed", f"{data['wind']['speed']} m/s")