import streamlit as st
import pandas as pd
import requests

API_KEY = "30dc3ec276c49ac523c3cfb2848e0"

# ------------------ SAFE GEOCODING FUNCTION ------------------
def get_lat_lon(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"

    try:
        res = requests.get(url).json()
        if not isinstance(res, list) or len(res) == 0:
            return None, None   # City not found
        return res[0]["lat"], res[0]["lon"]
    except:
        return None, None


# ------------------ FORECAST API ------------------
def get_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    return requests.get(url).json()


# ------------------ UI ------------------
st.title("📊 Weather Forecast (5 Days)")

city = st.text_input("Enter city name", "Delhi")

if st.button("Show Forecast"):
    lat, lon = get_lat_lon(city)

    if lat is None:
        st.error("❌ City not found or API limit reached.")
    else:
        data = get_forecast(lat, lon)

        if "list" not in data:
            st.error("❌ Failed to fetch forecast data. Possible API issue.")
        else:
            df = pd.json_normalize(data["list"])

            df["time"] = df["dt_txt"]
            df.set_index("time", inplace=True)

            st.markdown("<div class='card'><h3>📈 Forecast Trends</h3></div>", unsafe_allow_html=True)

            st.line_chart(df[["main.temp", "main.humidity", "wind.speed"]])

            st.write("### 🔍 Full Forecast Table")
            st.dataframe(df)
