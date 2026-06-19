from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv


def get_llm():
    load_dotenv(override=True)
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


#1st agent 
def build_search_agent():
    return create_agent(
        model=get_llm(),
        tools=[web_search],
    )


#2nd agent 
def build_reader_agent():
    return create_agent(
        model=get_llm(),
        tools=[scrape_url],
    )


#writer chain 

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

def build_writer_chain():
    return writer_prompt | get_llm() | StrOutputParser()


def build_critic_chain():
    return critic_prompt | get_llm() | StrOutputParser()

