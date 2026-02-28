import pandas as pd

def create_time_features(df, group_col='District', target='Avg_rainfall', lags=[1,2,3,7,14], windows=[3,7,14]):
    df = df.sort_values([group_col,'Date']).copy()
    for lag in lags:
        df[f'lag_{lag}'] = df.groupby(group_col)[target].shift(lag)
    for w in windows:
        df[f'roll_mean_{w}'] = df.groupby(group_col)[target].shift(1).rolling(window=w, min_periods=1).mean().reset_index(level=0, drop=True)
    return df
