from flask import Flask, request, jsonify
import gradio as gr
import os
import requests
from prompts import get_prompt

app = Flask(__name__)

# Load the Gemini API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def query_gemini_api(user_input):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "input": user_input,
        "model": "gemini"  # Specify the model if needed
    }
    response = requests.post("https://api.gemini.com/v1/query", headers=headers, json=data)
    return response.json().get("response", "Sorry, I couldn't process your request.")

def chatbot_response(user_input):
    prompt = get_prompt(user_input)
    response = query_gemini_api(prompt)
    return response

# Gradio interface
def launch_gradio():
    iface = gr.Interface(fn=chatbot_response, inputs="text", outputs="text", title="DevOps Chatbot", description="Ask me anything about DevOps!")
    iface.launch()

if __name__ == "__main__":
    launch_gradio()