from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from weather_models import (
    MODEL_EXPLANATIONS,
    MODEL_NAMES,
    compare_models,
    forecast_series,
)


DATA_DIR = Path(__file__).parent / "data"
TARGETS = {
    "Mean temperature (°C)": "temperature_mean_c",
    "Maximum temperature (°C)": "temperature_max_c",
    "Minimum temperature (°C)": "temperature_min_c",
    "Precipitation (mm)": "precipitation_mm",
    "Maximum wind speed (km/h)": "wind_speed_max_kmh",
}

st.set_page_config(
    page_title="Weather Forecasting Classroom",
    page_icon="🌦️",
    layout="wide",
)


@st.cache_data
def load_weather(path: str) -> pd.DataFrame:
    data = pd.read_csv(path, parse_dates=["date"])
    data = data.sort_values("date").drop_duplicates("date").set_index("date")
    return data


@st.cache_data(show_spinner="Training and comparing the forecasting models...")
def run_forecasts(
    series: pd.Series, horizon: int, test_days: int
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metrics, backtest_predictions = compare_models(series, test_days)
    future_predictions = {
        model_name: forecast_series(series, model_name, horizon)
        for model_name in MODEL_NAMES
    }
    return metrics, pd.DataFrame(future_predictions), backtest_predictions


st.title("Weather Forecasting: A Model Comparison Lab")
st.markdown(
    "Explore **real historical weather data**, build short-range forecasts, "
    "and compare simple baselines with statistical and machine-learning models."
)
st.info(
    "Teaching demo: this app forecasts from historical daily observations. "
    "It is not a live operational weather forecast."
)

data_files = sorted(DATA_DIR.glob("*_daily_weather.csv"))
if not data_files:
    st.error("No weather CSV found. Download the historical data first.")
    st.code("uv run python fetch_weather_data.py --city Mumbai --country India")
    st.stop()

with st.sidebar:
    st.header("Experiment settings")
    data_path = st.selectbox("Historical dataset", data_files, format_func=lambda path: path.name)
    data = load_weather(str(data_path))
    city = str(data["city"].iloc[0])
    country = str(data["country"].iloc[0])

    target_label = st.selectbox("Weather variable to predict", list(TARGETS))
    horizon = st.slider("Forecast horizon (days)", 1, 30, 14)
    training_years = st.slider("Years of training history", 2, 10, 5)
    max_test_days = min(60, max(7, len(data) // 5))
    test_days = st.slider(
        "Backtest holdout (days)",
        min_value=7,
        max_value=max_test_days,
        value=min(30, max_test_days),
    )

target_column = TARGETS[target_label]
series = data[target_column].dropna().astype(float)
series = series.loc[series.index >= series.index.max() - pd.Timedelta(days=365 * training_years)]

if len(series) <= max(test_days + 60, 365 * 2):
    st.error("Choose a longer training history or a dataset with more observations.")
    st.stop()

metrics, future_predictions, backtest_predictions = run_forecasts(
    series, horizon, test_days
)

latest = series.iloc[-1]
latest_date = series.index[-1]
forecast_end = future_predictions.iloc[-1]
best_model = metrics.iloc[0]

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Location", f"{city}, {country}")
metric2.metric(f"Latest {target_label.lower()}", f"{latest:,.2f}", latest_date.strftime("%Y-%m-%d"))
metric3.metric("Best backtest model (MAE)", str(best_model["Model"]))
metric4.metric("Forecast horizon", f"{horizon} days")

tab_forecast, tab_compare, tab_data, tab_lessons = st.tabs(
    ["Forecast", "Backtest comparison", "Explore the data", "Model guide"]
)

with tab_forecast:
    selected_models = st.multiselect(
        "Models to plot",
        options=MODEL_NAMES,
        default=MODEL_NAMES,
    )

    chart = go.Figure()
    chart.add_trace(
        go.Scatter(
            x=series.tail(365).index,
            y=series.tail(365).values,
            name="Observed",
            mode="lines",
            line=dict(color="#263238", width=2),
        )
    )
    for model_name in selected_models:
        chart.add_trace(
            go.Scatter(
                x=future_predictions.index,
                y=future_predictions[model_name],
                name=model_name,
                mode="lines+markers",
            )
        )
    chart.update_layout(
        title=f"{target_label}: historical observations and forecasts",
        xaxis_title="Date",
        yaxis_title=target_label,
        template="plotly_white",
        hovermode="x unified",
        height=520,
    )
    st.plotly_chart(chart, width="stretch")
    st.caption(
        "All forecasts are fitted to the same selected training window. "
        "Precipitation predictions are clipped at zero."
    )
    st.dataframe(
        future_predictions.loc[:, selected_models].round(2),
        width="stretch",
    )

with tab_compare:
    st.subheader(f"Out-of-sample test: last {test_days} days")
    st.caption(
        "Models are trained only on data before the holdout. Lower MAE and RMSE "
        "indicate smaller errors in the variable's native units."
    )
    metric_plot = go.Figure(
        go.Bar(
            x=metrics["MAE"],
            y=metrics["Model"],
            orientation="h",
            marker_color="#1976d2",
        )
    )
    metric_plot.update_layout(
        title="Mean absolute error by model (lower is better)",
        xaxis_title=f"MAE ({target_label})",
        yaxis_title="",
        template="plotly_white",
        height=430,
    )
    st.plotly_chart(metric_plot, width="stretch")
    st.dataframe(metrics.round(3), hide_index=True, width="stretch")

    backtest_chart = go.Figure()
    backtest_chart.add_trace(
        go.Scatter(x=series.index[-test_days:], y=series.iloc[-test_days:], name="Actual")
    )
    for model_name in selected_models:
        backtest_chart.add_trace(
            go.Scatter(
                x=backtest_predictions.index,
                y=backtest_predictions[model_name],
                name=model_name,
            )
        )
    backtest_chart.update_layout(
        title="Holdout: actual values vs model forecasts",
        xaxis_title="Date",
        yaxis_title=target_label,
        template="plotly_white",
        height=480,
    )
    st.plotly_chart(backtest_chart, width="stretch")

with tab_data:
    st.subheader("Historical observations")
    summary = data[target_column].describe().rename("Value").to_frame()
    left, right = st.columns(2)
    with left:
        st.write(
            f"**Source:** Open-Meteo Historical Weather API "
            f"(ERA5 reanalysis) · {city}, {country}"
        )
        st.write(
            f"**Coverage:** {data.index.min().date()} to {data.index.max().date()} "
            f"· **Rows:** {len(data):,}"
        )
        st.dataframe(summary.round(2), width="stretch")
    with right:
        st.download_button(
            "Download selected dataset",
            data=data.reset_index().to_csv(index=False).encode("utf-8"),
            file_name=data_path.name,
            mime="text/csv",
        )
    st.dataframe(data.tail(100), width="stretch")

with tab_lessons:
    st.subheader("What each model demonstrates")
    for model_name in MODEL_NAMES:
        with st.expander(model_name):
            st.write(MODEL_EXPLANATIONS[model_name])
    st.markdown(
        """
        **Suggested lesson:** start with Persistence as a baseline, then compare
        it to the seasonal and moving-average baselines. Next, discuss how
        lag-based regression and Random Forest use recent observations, and how
        Exponential Smoothing and ARIMA represent time-series structure.

        **Evaluation:** the final observations are held out in chronological
        order—never shuffled—so the test mimics predicting unseen future days.
        MAE is easy to interpret; RMSE penalizes larger misses more strongly.
        """
    )
    st.caption(
        "Historical reanalysis is not a station measurement or a substitute for "
        "a professional forecast. Weather changes quickly, and these models "
        "do not use current atmospheric conditions."
    )

st.caption("Weather data: Open-Meteo · https://open-meteo.com/")
