"""train_models.py
===================
Train multiple regression models on IPL ball‑by‑ball data, evaluate them, save the best
one (based on lowest Mean Absolute Error), plus artefacts required by the Streamlit app
(label encoders and scaler).

USAGE:
    python train_models.py --data ipl_data.csv

Outputs (in ./models):
    best_model.pkl          – scikit‑learn estimator
    scaler.pkl              – MinMaxScaler fitted on features
    encoders.pkl            – dict of LabelEncoders keyed by column name
    report.csv              – table of model → MAE sorted ascending
"""

import argparse
import joblib
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.svm import SVR

# Optional libraries – install if available
try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMRegressor
    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False

MODELS = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.001),
    "Polynomial2": Pipeline([("poly", PolynomialFeatures(degree=2, include_bias=False)),
                              ("lr", LinearRegression())]),
    "SVR": SVR(kernel="rbf", C=10, epsilon=0.1),
    "DecisionTree": DecisionTreeRegressor(max_depth=8, random_state=42),
    "RandomForest": RandomForestRegressor(n_estimators=300, max_depth=None, random_state=42, n_jobs=-1),
    "AdaBoost": AdaBoostRegressor(n_estimators=300, learning_rate=0.05, random_state=42),
    "GradientBoosting": GradientBoostingRegressor(random_state=42),
}
if HAS_XGB:
    MODELS["XGBoost"] = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6,
                                     subsample=0.8, colsample_bytree=0.8, objective="reg:squarederror",
                                     random_state=42)
if HAS_LGBM:
    MODELS["LightGBM"] = LGBMRegressor(n_estimators=500, learning_rate=0.05, max_depth=-1,
                                       subsample=0.8, colsample_bytree=0.8, random_state=42)

def preprocess(df: pd.DataFrame):
    # label encode high‑cardinality categoricals (same as original notebook)
    cat_cols = ["bat_team", "bowl_team", "venue", "batsman", "bowler"]

    label_encoders = {}
    for c in cat_cols:
        le = LabelEncoder()
        df[c] = le.fit_transform(df[c])
        label_encoders[c] = le

    feature_cols = ["bat_team", "bowl_team", "venue", "runs", "wickets",
                    "overs", "striker", "batsman", "bowler"]

    X = df[feature_cols].copy()
    y = df["total"].copy()
    return X, y, label_encoders

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", default="models")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)

    data = pd.read_csv(args.data)
    X, y, encoders = preprocess(data)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

    scaler = MinMaxScaler().fit(X_train)
    X_train_s = scaler.transform(X_train)
    X_test_s = scaler.transform(X_test)

    scores = {}
    for name, model in MODELS.items():
        model.fit(X_train_s, y_train)
        preds = model.predict(X_test_s)
        mae = mean_absolute_error(y_test, preds)
        scores[name] = mae
        print(f"{name:15s}  MAE = {mae:.2f}")

    # pick best (lowest MAE)
    best_name = min(scores, key=scores.get)
    best_model = MODELS[best_name]

    # persist artefacts
    joblib.dump(best_model, out_dir / "best_model.pkl")
    joblib.dump(encoders, out_dir / "encoders.pkl")
    joblib.dump(scaler, out_dir / "scaler.pkl")
    pd.Series(scores).sort_values().to_csv(out_dir / "report.csv", header=["MAE"])

    print(f"\nBest model: {best_name} (MAE={scores[best_name]:.2f}). Saved to '{out_dir}'.")

if __name__ == "__main__":
    main()

"""

"""app.py
========
A Streamlit web app that loads the best saved model plus scaler & encoders and provides
an interactive form for predicting the final innings total.

RUN:
    streamlit run app.py
"""

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

"""
