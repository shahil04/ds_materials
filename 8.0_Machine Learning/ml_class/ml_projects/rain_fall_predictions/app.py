import streamlit as st
import pandas as pd
import pickle

st.title("🌧 Rainfall Prediction App")

# Load saved model
with open("rainfall_prediction_model.pkl", "rb") as file:
    model_data = pickle.load(file)

# Your model inside pickle
best_rf_model = model_data["model"]     # change key if needed
feature_names = model_data["feature_names"]

st.subheader("Enter Weather Details")

# Input fields
pressure = st.number_input("Pressure (hPa)", value=1015.9)
dewpoint = st.number_input("Dew Point (°C)", value=19.9)
humidity = st.number_input("Humidity (%)", value=95)
cloud = st.number_input("Cloud (%)", value=81)
sunshine = st.number_input("Sunshine (hours)", value=0.0)
winddirection = st.number_input("Wind Direction (°)", value=40.0)
windspeed = st.number_input("Wind Speed (km/h)", value=13.7)

# Assemble input into DataFrame
input_data = pd.DataFrame([[
    pressure, dewpoint, humidity, cloud, sunshine, winddirection, windspeed
]], columns=['pressure', 'dewpoint', 'humidity', 'cloud', 'sunshine', 'winddirection', 'windspeed'])

# Predict button
if st.button("Predict Rainfall"):
    prediction = best_rf_model.predict(input_data)

    if prediction[0] == 1:
        st.success("🌧 Yes, Rainfall is likely to happen!")
    else:
        st.info("☀ No, Rainfall is not expected.")

