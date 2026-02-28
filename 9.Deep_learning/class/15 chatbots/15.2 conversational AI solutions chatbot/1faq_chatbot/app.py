# app.py
import streamlit as st
from responses import get_response

st.set_page_config(page_title="Customer Service Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Customer Service FAQ Chatbot")
st.write("Ask me anything about your order, refund, or delivery!")

# Session state to store chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input field
user_input = st.chat_input("Type your question...")

if user_input:
    bot_response = get_response(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", bot_response))

# Display chat history
for sender, message in st.session_state.history:
    if sender == "You":
        st.markdown(f"🧑‍💻 **You:** {message}")
    else:
        st.markdown(f"🤖 **Bot:** {message}")
