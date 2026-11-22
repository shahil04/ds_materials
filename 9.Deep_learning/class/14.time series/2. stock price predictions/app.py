from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="TSLA Stock Forecast",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def load_stock_data() -> pd.DataFrame:
    csv_path = Path(__file__).with_name("TSLA.CSV")
    data = pd.read_csv(csv_path)
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values("Date").set_index("Date")
    data = data.loc[:, ~data.columns.duplicated()]
    return data


def moving_average_forecast(
    series: pd.Series, horizon: int, window: int
) -> pd.Series:
    values = series.astype(float).copy()
    forecasts = []

    for _ in range(horizon):
        next_value = values.tail(window).mean()
        forecasts.append(next_value)
        values.loc[values.index[-1] + pd.offsets.BDay()] = next_value

    forecast_dates = pd.bdate_range(
        start=series.index[-1] + pd.offsets.BDay(),
        periods=horizon,
    )
    return pd.Series(forecasts, index=forecast_dates, name="Forecast")


def linear_trend_forecast(
    series: pd.Series, horizon: int, window: int
) -> pd.Series:
    recent = series.tail(window).astype(float)
    x = np.arange(len(recent))
    slope, intercept = np.polyfit(x, recent.to_numpy(), 1)

    future_x = np.arange(len(recent), len(recent) + horizon)
    forecasts = intercept + slope * future_x
    forecast_dates = pd.bdate_range(
        start=series.index[-1] + pd.offsets.BDay(),
        periods=horizon,
    )
    return pd.Series(forecasts, index=forecast_dates, name="Forecast")


def arima_forecast(series: pd.Series, horizon: int) -> pd.Series:
    try:
        from statsmodels.tsa.arima.model import ARIMA

        model = ARIMA(series.tail(500), order=(5, 1, 0))
        fitted = model.fit()
        forecast = fitted.forecast(steps=horizon)
        forecast.index = pd.bdate_range(
            start=series.index[-1] + pd.offsets.BDay(),
            periods=horizon,
        )
        forecast.name = "Forecast"
        return forecast
    except Exception:
        return linear_trend_forecast(series, horizon, 60)


def make_forecast(
    series: pd.Series, method: str, horizon: int, window: int
) -> pd.Series:
    if method == "Moving Average":
        return moving_average_forecast(series, horizon, window)
    if method == "ARIMA":
        return arima_forecast(series, horizon)
    return linear_trend_forecast(series, horizon, window)


def calculate_metrics(
    series: pd.Series, method: str, window: int
) -> tuple[float, float, float]:
    test_size = min(10 if method == "ARIMA" else 30, max(10, len(series) // 5))
    actual = series.tail(test_size).to_numpy(dtype=float)
    predictions = []

    for i in range(len(series) - test_size, len(series)):
        history = series.iloc[:i]
        if len(history) < max(window, 5):
            continue
        prediction = make_forecast(history, method, 1, window).iloc[0]
        predictions.append(prediction)

    if not predictions:
        return 0.0, 0.0, 0.0

    predictions = np.array(predictions)
    actual = actual[-len(predictions):]
    mae = np.mean(np.abs(actual - predictions))
    rmse = np.sqrt(np.mean((actual - predictions) ** 2))
    mape = np.mean(np.abs((actual - predictions) / actual)) * 100
    return float(mae), float(rmse), float(mape)


data = load_stock_data()

st.title("TSLA Stock Price Forecast")
st.caption("Interactive historical analysis and short-term close-price forecasting")

if data.empty:
    st.error("TSLA.CSV could not be loaded.")
    st.stop()

with st.sidebar:
    st.header("Forecast Controls")
    method = st.selectbox(
        "Forecast method",
        ["Moving Average", "Linear Trend", "ARIMA"],
    )
    horizon = st.slider("Forecast horizon (business days)", 1, 30, 10)
    window = st.slider("Training window (days)", 10, 200, 60)
    history_days = st.slider("Chart history (days)", 30, 600, 180)
    st.divider()
    st.caption("Models use the historical closing price.")

close = data["Close"].astype(float)
forecast = make_forecast(close, method, horizon, window)

latest_close = close.iloc[-1]
previous_close = close.iloc[-2]
daily_change = latest_close - previous_close
daily_change_pct = (daily_change / previous_close) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Latest close", f"${latest_close:,.2f}", f"{daily_change:+,.2f}")
col2.metric(
    "Daily change",
    f"{daily_change_pct:+.2f}%",
)
col3.metric("Forecast horizon", f"{horizon} days")
col4.metric("Forecast end", f"${forecast.iloc[-1]:,.2f}")

tab1, tab2, tab3 = st.tabs(["Price Forecast", "Market Trends", "Raw Data"])

with tab1:
    chart = go.Figure()
    chart.add_trace(
        go.Scatter(
            x=close.tail(history_days).index,
            y=close.tail(history_days).values,
            mode="lines",
            name="Historical Close",
            line=dict(color="#1f77b4", width=2),
        )
    )
    chart.add_trace(
        go.Scatter(
            x=forecast.index,
            y=forecast.values,
            mode="lines+markers",
            name=f"{method} Forecast",
            line=dict(color="#ff7f0e", width=3),
        )
    )
    chart.update_layout(
        title="TSLA Closing Price with Forecast",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode="x unified",
        template="plotly_white",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(chart, width="stretch")

    mae, rmse, mape = calculate_metrics(close, method, window)
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Backtest MAE", f"${mae:,.2f}")
    metric2.metric("Backtest RMSE", f"${rmse:,.2f}")
    metric3.metric("Backtest MAPE", f"{mape:.2f}%")

    forecast_table = forecast.rename("Predicted Close").to_frame()
    forecast_table["Predicted Close"] = forecast_table["Predicted Close"].round(2)
    st.subheader("Forecast Values")
    st.dataframe(forecast_table, width="stretch")

with tab2:
    trend1, trend2 = st.columns(2)

    with trend1:
        candlestick = go.Figure(
            data=[
                go.Candlestick(
                    x=data.tail(history_days).index,
                    open=data.tail(history_days)["Open"],
                    high=data.tail(history_days)["High"],
                    low=data.tail(history_days)["Low"],
                    close=data.tail(history_days)["Close"],
                )
            ]
        )
        candlestick.update_layout(
            title="Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            height=420,
            xaxis_rangeslider_visible=False,
        )
        st.plotly_chart(candlestick, width="stretch")

    with trend2:
        moving_average = close.rolling(window=window, min_periods=1).mean()
        trend_chart = go.Figure()
        trend_chart.add_trace(
            go.Scatter(
                x=close.tail(history_days).index,
                y=close.tail(history_days).values,
                name="Close",
                line=dict(color="#1f77b4"),
            )
        )
        trend_chart.add_trace(
            go.Scatter(
                x=moving_average.tail(history_days).index,
                y=moving_average.tail(history_days).values,
                name=f"{window}-Day Moving Average",
                line=dict(color="#d62728"),
            )
        )
        trend_chart.update_layout(
            title="Close Price and Moving Average",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            height=420,
        )
        st.plotly_chart(trend_chart, width="stretch")

with tab3:
    st.subheader("Historical TSLA Data")
    st.dataframe(data.tail(250), width="stretch")
    st.download_button(
        "Download CSV",
        data.to_csv().encode("utf-8"),
        file_name="TSLA.csv",
        mime="text/csv",
    )

st.warning(
    "For educational purposes only. Forecasts are not financial advice.",
    icon="⚠️",
)
