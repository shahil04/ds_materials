    # bengaluru_app.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and location list
model = joblib.load("bengaluru_house_model.pkl")
locations = joblib.load("location_list.pkl")

# Streamlit UI
st.set_page_config(page_title="Bengaluru House Price Predictor", layout="centered")
st.title("🏠 Bengaluru House Price Predictor")

st.sidebar.header("Input House Details")

location = st.sidebar.selectbox("Select Location", sorted(locations))
total_sqft = st.sidebar.number_input("Total Square Feet", min_value=300.0, max_value=10000.0, value=1000.0)
bhk = st.sidebar.slider("Bedrooms (BHK)", 1, 10, 2)
bath = st.sidebar.slider("Bathrooms", 1, 10, 2)

if st.sidebar.button("Predict Price"):
    input_data = pd.DataFrame({
        "location": [location],
        "total_sqft": [total_sqft],
        "bhk": [bhk],
        "bath": [bath]
    })
    
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Estimated Price: ₹{prediction:.2f} Lakhs")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Scikit-Learn")
