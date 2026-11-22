# Weather Forecasting Model Comparison Lab

A Streamlit teaching app that uses real historical daily weather data to
demonstrate forecasting baselines, time-series models, backtesting, and error
metrics.

## Set up and run with uv

From this folder:

```powershell
uv sync
uv run python fetch_weather_data.py --city Mumbai --country India
uv run streamlit run app.py
```

The fetch script geocodes the selected city and downloads daily observations
from the Open-Meteo Historical Weather API. By default, it downloads from
2015-01-01 through seven days ago and saves a CSV under `data/`.

Fetch another location or date range:

```powershell
uv run python fetch_weather_data.py --city Pune --country India --start-date 2018-01-01
```

## Models included

- Persistence, 7-day seasonal naive, moving average, and seasonal climatology
  baselines
- Linear regression and Random Forest with lag and annual-seasonality features
- Holt-Winters exponential smoothing with annual seasonality
- ARIMA(2, 1, 2)

The app compares them on a chronological holdout using MAE and RMSE. The
holdout is never shuffled. Forecasts are educational demonstrations based on
historical observations—not live operational weather predictions.

## Data source

Data comes from the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api),
which provides gridded reanalysis data (ERA5). Variables include mean, maximum,
and minimum temperature, precipitation sum, and maximum wind speed.
