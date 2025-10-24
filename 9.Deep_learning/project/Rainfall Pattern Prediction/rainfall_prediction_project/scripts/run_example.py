# Quick example to train a RandomForest on the sample data (very small toy example)
import pandas as pd
from src.data_prep import clean_dates, load_raw
from src.features import create_time_features
from src.models import build_rf_pipeline, save_model
from src.evaluate import rmse, mae

df = load_raw('data/raw/sample_rainfall.csv')
df = clean_dates(df)
df = create_time_features(df)
df = df.dropna(subset=['lag_1'])  # small dataset -> drop early rows

features = ['lag_1','lag_2','lag_3','roll_mean_7','Day','Month']
cat = ['District']
num = ['lag_1','lag_2','lag_3','roll_mean_7','Day','Month']

if len(df) < 10:
    print('Dataset small - this is a toy run.')

X = df[num + cat]
y = df['Avg_rainfall']

# simple time split: last 20% as test
split = int(0.8 * len(df))
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]

model = build_rf_pipeline(num, cat)
model.fit(X_train, y_train)
preds = model.predict(X_test)

print('RMSE:', rmse(y_test, preds), 'MAE:', mae(y_test, preds))
import os
os.makedirs("models", exist_ok=True)

save_model(model, 'models/rf_model.joblib')
print('Saved models/rf_model.joblib')
