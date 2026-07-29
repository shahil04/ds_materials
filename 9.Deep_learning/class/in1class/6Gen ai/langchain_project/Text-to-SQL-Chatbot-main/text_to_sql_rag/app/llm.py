import os

from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv

load_dotenv()

# llm = ChatGoogleGenerativeAI(
#     model="gemini-3.5-flash",
#     temperature=0
# )

from langchain_openai import ChatOpenAI
# Create ChatGPT model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def generate_sql(prompt):

    response = llm.invoke(prompt)

    return response.content.strip()