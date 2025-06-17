# prompt: create a streamlit project code for above model  only use numerical columns months_as_customer	age	policy_annual_premium	auto_year	umbrella_limit as x 

import streamlit as st
import pandas as pd
import pickle

# Load the trained model
filename = 'logistic_model.pkl'
loaded_model = pickle.load(open(filename, 'rb'))

st.title("Insurance Claim Fraud Prediction")

st.write("""
This app predicts whether an insurance claim is fraudulent based on several factors.
""")

# Define input fields for numerical features
months_as_customer = st.number_input('Months as Customer', min_value=0, max_value=500, value=100)
age = st.number_input('Age', min_value=18, max_value=100, value=30)
policy_annual_premium = st.number_input('Policy Annual Premium', min_value=0.0, max_value=2500.0, value=1000.0)
auto_year = st.number_input('Auto Year', min_value=1980, max_value=2023, value=2010)
umbrella_limit = st.number_input('Umbrella Limit', min_value=-10000000, max_value=10000000, value=0)


# Create a button to make a prediction
if st.button('Predict Fraud'):
    # Create a DataFrame from the input values
    input_data = pd.DataFrame({
        'months_as_customer': [months_as_customer],
        'age': [age],
        'policy_annual_premium': [policy_annual_premium],
        'auto_year': [auto_year],
        'umbrella_limit': [umbrella_limit],
    })

    # Select only the numerical columns used for prediction based on the original code
    numerical_cols_for_prediction = ['months_as_customer', 'age', 'policy_annual_premium', 'auto_year', 'umbrella_limit']
    input_data_for_prediction = input_data[numerical_cols_for_prediction]

    # Make the prediction
    prediction = loaded_model.predict(input_data_for_prediction)

    # Display the prediction
    if prediction[0] == 'Y':
        st.write("Prediction: Fraud Reported (Y)")
    else:
        st.write("Prediction: No Fraud Reported (N)")

