from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

model = ChatOpenAI()
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
<<<<<<< HEAD
result = chain.invoke({"question": "What is the capital of Peru?"})
=======
result = chain.invoke({"question": "What is the capital of India?"})
>>>>>>> 8db78abd3048b3607821d2e78dc198c0324f1839
print(result)
