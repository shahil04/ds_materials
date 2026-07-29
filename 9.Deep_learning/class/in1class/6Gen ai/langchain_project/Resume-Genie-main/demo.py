# # -*- coding: utf-8 -*-
# """
# Created on Tue Jan 20 13:18:29 2026

# @author: User
# """

# import streamlit as st
# from PIL import Image

# logo = Image.open("logo.png")
# st.sidebar.image(logo,width=80)

# st.sidebar.markdown("**Resume Genie**")

# st.title("Hello World!!")
# st.write("Welcome to my first Streamlit App")

import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
# llm DEMO using langchain
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model='gpt-4.1-mini')

result = llm.invoke("What is the capital of India")

print(result)