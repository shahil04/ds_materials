import streamlit as st
import pandas as pd 


st.title("App Title")

st.write("write any text")


df = pd.DataFrame({"Category": ["A", "B", "C"], "Value": [10, 20, 30]})

st.bar_chart(df, x="Category", y="Value")