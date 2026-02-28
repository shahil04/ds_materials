import pandas as pd
import numpy as np
from pathlib import Path

def load_raw(path: str):
    df = pd.read_csv(path)
    return df

def clean_dates(df: pd.DataFrame):
    df = df.dropna(subset=['Date']).copy()
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
    df = df.dropna(subset=['Date']).copy()
    df['Day'] = df['Date'].dt.day
    df['Weekday'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    return df

def save_processed(df: pd.DataFrame, out_path: str):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)

if __name__ == '__main__':
    df = load_raw('data/raw/sample_rainfall.csv')
    dfc = clean_dates(df)
    save_processed(dfc, 'data/processed/processed_rainfall.csv')
    print('Saved processed data to data/processed/processed_rainfall.csv')
