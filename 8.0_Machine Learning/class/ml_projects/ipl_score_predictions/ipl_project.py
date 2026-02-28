

# """app.py
# ========
# A Streamlit web app that loads the best saved model plus scaler & encoders and provides
# an interactive form for predicting the final innings total.

# RUN:
#     streamlit run app.py
# """

import streamlit as st
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent / "models"
encoders = joblib.load(MODEL_DIR / "encoders.pkl")
scaler = joblib.load(MODEL_DIR / "scaler.pkl")
model = joblib.load(MODEL_DIR / "best_model.pkl")

st.set_page_config(page_title="IPL Score Predictor", page_icon="🏏", layout="centered")
st.title("🏏 IPL Final Score Predictor (ML edition)")

# Convenience – sort for nicer UX
venues = sorted(encoders["venue"].classes_)
bat_teams = sorted(encoders["bat_team"].classes_)
bowl_teams = sorted(encoders["bowl_team"].classes_)
batsmen = sorted(encoders["batsman"].classes_)
bowlers = sorted(encoders["bowler"].classes_)

with st.form("predict_form"):
    c1, c2 = st.columns(2)
    venue = c1.selectbox("Venue", venues)
    bat_team = c1.selectbox("Batting team", bat_teams)
    bowl_team = c1.selectbox("Bowling team", bowl_teams)
    striker = c1.selectbox("Current striker", batsmen)
    bowler = c1.selectbox("Current bowler", bowlers)

    runs = c2.number_input("Current runs scored", min_value=0, value=0, step=1)
    wickets = c2.number_input("Wickets down", min_value=0, value=0, step=1)
    overs = c2.number_input("Overs completed", min_value=0.0, max_value=20.0, value=0.0, step=0.1)
    striker_ind = c2.number_input("Striker indicator (0 or 1)", min_value=0, max_value=1, value=0, step=1)

    submitted = st.form_submit_button("Predict")

if submitted:
    # Encode categoricals
    encoded_inputs = [
        encoders["bat_team"].transform([bat_team])[0],
        encoders["bowl_team"].transform([bowl_team])[0],
        encoders["venue"].transform([venue])[0],
        runs,
        wickets,
        overs,
        striker_ind,
        encoders["batsman"].transform([striker])[0],
        encoders["bowler"].transform([bowler])[0],
    ]

    features = np.array(encoded_inputs).reshape(1, -1)
    features_scaled = scaler.transform(features)
    pred_total = model.predict(features_scaled)[0]

    st.success(f"🏆 Predicted Final Score: **{pred_total:.0f} runs**")

