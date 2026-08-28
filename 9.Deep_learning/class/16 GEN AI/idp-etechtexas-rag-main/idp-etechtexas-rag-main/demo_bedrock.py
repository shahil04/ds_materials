from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="openai.gpt-oss-120b",
    messages=[{"role": "user", "content": "What is Amazon Bedrock?"}],
)

print(response.choices[0].message.content)


# from dotenv import load_dotenv
# import os

# load_dotenv()

# print("API key loaded:", bool(os.getenv("OPENAI_API_KEY")))
# print("Base URL:", os.getenv("OPENAI_BASE_URL"))
