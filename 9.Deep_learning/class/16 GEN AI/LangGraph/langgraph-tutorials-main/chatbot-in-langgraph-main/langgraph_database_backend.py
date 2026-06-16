from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

# Load environment variables such as API keys from a .env file.
load_dotenv()

# Initialize the language model used by the chatbot.
llm = ChatOpenAI()

# Define the shared state structure for the LangGraph workflow.
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Main chatbot node: receives the conversation state and returns a model response.
def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {"messages": [response]}

# Connect to the SQLite database used for conversation checkpointing.
conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# Create a checkpointer so the graph can persist chat state between turns.
checkpointer = SqliteSaver(conn=conn)

# Build the LangGraph workflow and connect the nodes.
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile the graph with persistence enabled.
chatbot = graph.compile(checkpointer=checkpointer)

# Return all thread IDs that currently have saved checkpoints.
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)


