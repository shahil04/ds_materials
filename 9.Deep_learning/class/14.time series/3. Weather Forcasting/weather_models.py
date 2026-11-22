"""Small, interpretable forecasting examples for daily weather series."""

import warnings

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


MODEL_NAMES = [
    "Persistence",
    "7-day Seasonal Naive",
    "Moving Average",
    "Seasonal Climatology",
    "Linear Regression (lags)",
    "Random Forest (lags)",
    "Exponential Smoothing",
    "ARIMA",
]

MODEL_EXPLANATIONS = {
    "Persistence": "Repeats the last observed value. A simple baseline.",
    "7-day Seasonal Naive": "Repeats the value from seven days earlier.",
    "Moving Average": "Recursively averages the last seven observations.",
    "Seasonal Climatology": "Uses the historical average for nearby calendar days.",
    "Linear Regression (lags)": "Learns from recent lags and annual sine/cosine features.",
    "Random Forest (lags)": "Learns nonlinear relationships from the same lag features.",
    "Exponential Smoothing": "Holt-Winters model with trend and annual seasonality.",
    "ARIMA": "Autoregressive integrated moving average with order (2, 1, 2).",
}

LAGS = (1, 2, 3, 7, 14, 30)


def _validate_series(series: pd.Series) -> pd.Series:
    cleaned = series.dropna().astype(float).sort_index()
    if len(cleaned) < 60:
        raise ValueError("At least 60 days of non-missing observations are required.")
    if not isinstance(cleaned.index, pd.DatetimeIndex):
        raise TypeError("Weather series must have a DatetimeIndex.")
    return cleaned


def _lag_features(history: pd.Series, forecast_date: pd.Timestamp) -> list[float]:
    values = [float(history.iloc[-lag]) for lag in LAGS]
    annual_phase = 2 * np.pi * forecast_date.dayofyear / 365.25
    return values + [float(np.sin(annual_phase)), float(np.cos(annual_phase))]


def _lagged_training_data(series: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    features = []
    targets = []
    for position in range(max(LAGS), len(series)):
        features.append(
            _lag_features(series.iloc[:position], pd.Timestamp(series.index[position]))
        )
        targets.append(float(series.iloc[position]))
    return np.asarray(features), np.asarray(targets)


def _forecast_lag_model(
    series: pd.Series, horizon: int, model_name: str
) -> np.ndarray:
    if len(series) <= max(LAGS) + 10:
        raise ValueError("Lag models need more historical observations.")

    x_train, y_train = _lagged_training_data(series)
    if model_name == "Linear Regression (lags)":
        model = LinearRegression()
    else:
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_leaf=3,
            random_state=42,
            n_jobs=-1,
        )
    model.fit(x_train, y_train)

    history = series.copy()
    predictions = []
    for _ in range(horizon):
        next_date = history.index[-1] + pd.Timedelta(days=1)
        next_value = float(model.predict([_lag_features(history, next_date)])[0])
        predictions.append(next_value)
        history.loc[next_date] = next_value
    return np.asarray(predictions)


def forecast_series(
    series: pd.Series, model_name: str, horizon: int
) -> pd.Series:
    """Fit one demonstration model and return a forecast indexed by future dates."""
    if horizon < 1:
        raise ValueError("Forecast horizon must be at least one day.")
    history = _validate_series(series)
    future_dates = pd.date_range(
        history.index[-1] + pd.Timedelta(days=1),
        periods=horizon,
        freq="D",
    )

    if model_name == "Persistence":
        predictions = np.repeat(history.iloc[-1], horizon)
    elif model_name == "7-day Seasonal Naive":
        seasonal_period = 7
        predictions = []
        extended = history.to_list()
        for _ in range(horizon):
            value = extended[-seasonal_period]
            predictions.append(value)
            extended.append(value)
    elif model_name == "Moving Average":
        predictions = []
        extended = history.to_list()
        for _ in range(horizon):
            value = float(np.mean(extended[-7:]))
            predictions.append(value)
            extended.append(value)
    elif model_name == "Seasonal Climatology":
        day_of_year = history.index.dayofyear.to_numpy()
        values = history.to_numpy()
        predictions = []
        for forecast_date in future_dates:
            distance = np.abs(day_of_year - forecast_date.dayofyear)
            circular_distance = np.minimum(distance, 366 - distance)
            nearby = values[circular_distance <= 7]
            predictions.append(float(np.mean(nearby)) if len(nearby) else float(np.mean(values)))
    elif model_name in ("Linear Regression (lags)", "Random Forest (lags)"):
        predictions = _forecast_lag_model(history, horizon, model_name)
    elif model_name == "Exponential Smoothing":
        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = ExponentialSmoothing(
                history.to_numpy(),
                trend="add",
                damped_trend=True,
                seasonal="add",
                seasonal_periods=365,
                initialization_method="estimated",
            )
            fitted = model.fit(optimized=True)
        predictions = fitted.forecast(horizon)
    elif model_name == "ARIMA":
        from statsmodels.tsa.arima.model import ARIMA

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fitted = ARIMA(history.to_numpy(), order=(2, 1, 2)).fit()
        predictions = fitted.forecast(steps=horizon)
    else:
        raise ValueError(f"Unknown forecast model: {model_name}")

    predictions = np.asarray(predictions, dtype=float)
    if "precipitation" in str(series.name).casefold():
        predictions = np.maximum(predictions, 0)
    if len(predictions) != horizon or not np.isfinite(predictions).all():
        raise ValueError(f"{model_name} produced invalid forecast values.")
    return pd.Series(predictions, index=future_dates, name=model_name)


def compare_models(
    series: pd.Series, test_days: int
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare models on one chronological holdout period."""
    history = _validate_series(series)
    if not 1 <= test_days < len(history) - 60:
        raise ValueError("Holdout must leave at least 60 training observations.")

    train = history.iloc[:-test_days]
    actual = history.iloc[-test_days:]
    forecasts = {}
    rows = []

    for model_name in MODEL_NAMES:
        predicted = forecast_series(train, model_name, test_days)
        predicted_values = predicted.to_numpy()
        actual_values = actual.to_numpy()
        errors = actual_values - predicted_values
        forecasts[model_name] = predicted
        rows.append(
            {
                "Model": model_name,
                "MAE": float(np.mean(np.abs(errors))),
                "RMSE": float(np.sqrt(np.mean(errors**2))),
            }
        )

    return pd.DataFrame(rows).sort_values("MAE"), pd.DataFrame(forecasts, index=actual.index)
