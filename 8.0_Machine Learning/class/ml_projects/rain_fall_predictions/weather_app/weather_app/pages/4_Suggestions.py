import streamlit as st

st.title("💡 Smart Weather Suggestions")

st.markdown("""<div class='card'>
<h3>✨ Based on Temperature</h3>
<li>Stay hydrated above 30°C</li>
<li>Wear jacket below 15°C</li>
</div>

<div class='card'>
<h3>🌧 Based on Rain Chances</h3>
<li>Carry umbrella if rainfall predicted</li>
<li>Avoid travel during heavy showers</li>
</div>

<div class='card'>
<h3>🌬 Based on Wind</h3>
<li>Avoid rooftops if wind > 25 km/h</li>
<li>Secure outdoor objects during storms</li>
</div>
""", unsafe_allow_html=True)