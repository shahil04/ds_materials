import streamlit as st
import pandas as pd
import requests
import pickle
from pathlib import Path

st.title("🌧 AI Rainfall Prediction")

# ------------------------------ LOAD MODEL ------------------------------
model_path = Path("rainfall_prediction_model.pkl")
if not model_path.exists():
    st.warning("⚠ Model file not found. Using placeholder dummy model.")
    best_rf_model = None
else:
    with open(model_path, "rb") as f:
        model_obj = pickle.load(f)
        best_rf_model = model_obj.get("model", None)


# ------------------------------ SESSION STATE ------------------------------
if "mode" not in st.session_state:
    st.session_state.mode = None   # None, "city", "manual"

# Reset button logic
def set_mode_city():
    st.session_state.mode = "city"

def set_mode_manual():
    st.session_state.mode = "manual"

def reset_mode():
    st.session_state.mode = None


# ------------------------------ API FUNCTIONS ------------------------------
API_KEY = "30dc3ec276c49ac523473c3cfb2848e0"

def get_lat_lon(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    res = requests.get(url).json()
    if not res:
        return None, None
    return res[0]['lat'], res[0]['lon']

def get_forecast(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    return requests.get(url).json()

def api_to_model_input(entry):
    temp = entry['main']['temp']
    humidity = entry['main']['humidity']
    pressure = entry['main']['pressure']
    cloud = entry['clouds']['all']
    windspeed = entry['wind']['speed']
    winddirection = entry['wind']['deg']

    dewpoint = temp - ((100 - humidity) / 5)

    sunshine = 10 if cloud < 20 else 5 if cloud < 60 else 1

    return [pressure, dewpoint, humidity, cloud, sunshine, winddirection, windspeed]


# ------------------------------ MAIN UI ------------------------------
if st.session_state.mode is None:
    st.markdown("<div class='card'><h3>Select Prediction Method</h3></div>", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        st.button("🏙 Predict by City Name", use_container_width=True, on_click=set_mode_city)

    with colB:
        st.button("✍ Predict by Manual Input", use_container_width=True, on_click=set_mode_manual)

# ======================================================================
# 1️⃣ CITY NAME MODE
# ======================================================================
if st.session_state.mode == "city":
    st.subheader("🏙 Predict Rainfall by City Name")

    city = st.text_input("Enter City", "Delhi")

    if st.button("Fetch & Predict"):
        lat, lon = get_lat_lon(city)

        if lat is None:
            st.error("❌ City not found!")
        else:
            forecast = get_forecast(lat, lon)
            first_entry = forecast['list'][0]

            input_data = api_to_model_input(first_entry)

            input_df = pd.DataFrame([input_data], 
                columns=['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine', 'winddirection', 'windspeed'])

            st.write("### Extracted Weather Inputs:")
            st.dataframe(input_df)

            if best_rf_model is None:
                st.error("❌ Rainfall model not found!")
            else:
                pred = best_rf_model.predict(input_df)[0]

                if pred == 1:
                    st.success(f"🌧 YES! Rainfall likely in **{city}**.")
                else:
                    st.info(f"☀ NO! Rainfall not expected in **{city}**.")

    st.button("⬅ Back", on_click=reset_mode)


# ======================================================================
# 2️⃣ MANUAL INPUT MODE
# ======================================================================
if st.session_state.mode == "manual":
    st.subheader("✍ Predict Rainfall by Filling Weather Details")

    col1, col2, col3 = st.columns(3)

    pressure = col1.number_input("Pressure (hPa)", value=1015.0)
    dewpoint = col2.number_input("Dew Point (°C)", value=20.0)
    humidity = col3.number_input("Humidity (%)", value=60)

    cloud = col1.number_input("Cloud (%)", value=40)
    sunshine = col2.number_input("Sunshine (hours)", value=6)
    winddirection = col3.number_input("Wind Direction (°)", value=180)
    windspeed = col1.number_input("Wind Speed (km/h)", value=8.0)

    input_df = pd.DataFrame([[pressure, dewpoint, humidity, cloud, sunshine, winddirection, windspeed]],
                            columns=['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine', 'winddirection', 'windspeed'])

    st.write("### Input Data")
    st.dataframe(input_df)

    if st.button("Predict Rainfall"):
        if best_rf_model is None:
            st.error("❌ Model not found!")
        else:
            pred = best_rf_model.predict(input_df)[0]

            if pred == 1:
                st.success("🌧 Rainfall Likely")
            else:
                st.info("☀ No Rainfall Expected")

    st.button("⬅ Back", on_click=reset_mode)
