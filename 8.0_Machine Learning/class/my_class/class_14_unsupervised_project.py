# logistic_regression_model predictions
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained regression model
with open("kmeans_model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("Customer segment analysis")
st.write("Enter the required details of Customer.")

# Input fields for user
age = st.number_input("Age", min_value=0)
Annual_Income  = st.number_input("Annual Income ", min_value=0)

gender = st.selectbox("gender (eg. 0 for male 1 for female)", [0, 1])

# Predict button
if st.button("Predict Loan Amount"):
    # Create a DataFrame with user input
    input_data = pd.DataFrame(
        [[age, Annual_Income]],
        columns=["age","Annual_Income"]
    )
    
    # Predict loan amount
    customer_segment = model.predict(input_data)[0]
    
    if customer_segment==0:
        st.success(f"modrate customer {customer_segment} 20%")
    elif customer_segment==1:
        st.success(f"premium customer 70% {customer_segment}")
    elif customer_segment==2:
        st.success(f"medium customer{customer_segment} 30%" )
    elif customer_segment==3:
        st.success(f"high income low spending customer {customer_segment} 90%")

    else:
        st.success(f"low income low spending customer {customer_segment} 10%")

#  streamlit run
# python -m streamlit run unsupervised_project.py

