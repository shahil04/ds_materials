import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.set_page_config(
    page_title="Weather & Rainfall App",
    page_icon="🌦",
    layout="wide",
)

# ---- Custom Dark Theme CSS ----
dark_css = """<style>
body {
    background-color: #0e1117;
    color: #f0f2f6;
}
[data-testid="stSidebar"] {
    background-color: #111418 !important;
}
.card {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0px;
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
}
.metric-card {
    background: rgba(0, 0, 0, 0.35);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
}
h1, h2, h3, h4 {
    font-family: 'Poppins', sans-serif;
}
</style>"""
st.markdown(dark_css, unsafe_allow_html=True)

# Load lottie animation
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

weather_anim = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jmBauI.json")

st.title("🌦 Modern Weather & AI Rainfall App")
st.caption("Powered by OpenWeather API + Your ML Rainfall Model")

col1, col2 = st.columns([1,2])

with col1:
    if weather_anim:
        st_lottie(weather_anim, height=260, key="weather")
    else:
        st.image("https://openweathermap.org/themes/openweathermap/assets/vendor/owm/img/icons/logo_60x60.png", width=120)

with col2:
    st.markdown("""<div class="card">
    <h2>✨ Welcome!</h2>
    <p>This modern AI-powered dashboard gives you:</p>
    <ul>
        <li><b>Today's Weather</b> with real-time data</li>
        <li><b>Rainfall Predictions</b> using your ML model</li>
        <li><b>5-Day Forecast</b> in interactive charts</li>
        <li><b>Smart Suggestions</b> based on weather</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

st.write("### 👈 Use the left sidebar to navigate through the features.")