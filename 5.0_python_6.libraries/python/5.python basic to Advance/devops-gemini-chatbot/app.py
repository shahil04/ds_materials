from flask import Flask, request, jsonify
import gradio as gr
from src.chatbot import Chatbot

app = Flask(__name__)
chatbot = Chatbot()

def respond_to_query(user_input):
    response = chatbot.get_response(user_input)
    return response

iface = gr.Interface(fn=respond_to_query, 
                     inputs="text", 
                     outputs="text", 
                     title="DevOps Chatbot",
                     description="Ask your DevOps-related questions and get answers from the chatbot powered by Gemini API.")

if __name__ == "__main__":
    iface.launch()