# logistic_regression_model predictions
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the trained regression model
with open("logistic_regression_model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("Loan Amount Prediction")
st.write("Enter the required details to predict the loan amount.")

# Input fields for user
applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount_term = st.number_input("Loan Amount Term", min_value=0)
LoanAmount = st.number_input("Loan Amount ", min_value=0)
credit_history = st.selectbox("Credit History", [0, 1])

# Predict button
if st.button("Predict Loan Amount"):
    # Create a DataFrame with user input
    input_data = pd.DataFrame(
        [[applicant_income, coapplicant_income, loan_amount_term,LoanAmount, credit_history]],
        columns=["ApplicantIncome","CoapplicantIncome","Loan_Amount_Term","LoanAmount","Credit_History"]
    )
    
    # Predict loan amount
    predicted_loan_amount = model.predict(input_data)[0]
    
    if predicted_loan_amount:
        st.success(f"Hurry you are Eligible for Loan Amount: {predicted_loan_amount}")
    else:
        st.success(f"OH! No: No Eligible for Loan: {predicted_loan_amount}")

st.write("Upload a dataset for batch predictions")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    predictions = model.predict(df)
    df["Predicted Loan Amount"] = predictions
    st.write(df)
    df.to_csv("predicted_loans.csv", index=False)
    st.download_button("Download Predictions", "predicted_loans.csv")

# streamlit run streamlit_loan.py