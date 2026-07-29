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
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file or environment variables.")

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.2)
result = llm.invoke("What is the capital of India")
print(result.content)