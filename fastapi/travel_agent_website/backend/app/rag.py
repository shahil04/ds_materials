import os
from typing import List, Tuple

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from .config import settings

KB_FILE = "rag_store.faiss"

def get_embeddings():
    return OpenAIEmbeddings(openai_api_key=settings.openai_api_key)


def get_vectorstore():
    if os.path.exists(KB_FILE):
        return FAISS.load_local(KB_FILE, get_embeddings())
    return None


def build_knowledge_base(documents: List[Tuple[str, str]]):
    # documents: list of (title, text)
    texts = [f"{title}\n{body}" for title, body in documents]
    vs = FAISS.from_texts(texts, get_embeddings())
    vs.save_local(KB_FILE)
    return vs


def rag_response(query: str):
    vs = get_vectorstore()
    if vs is None:
        raise RuntimeError("Knowledge base is not initialized")

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are Traveller Buddy, an intelligent travel assistant.
Use provided context to answer the question.
Context:\n{context}\n
Question: {question}\n
Always include day-wise itinerary, estimated cost, hotels, transport plans and tips.
""",
    )

    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=settings.openai_api_key, temperature=0.2, max_tokens=450),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        prompt=prompt,
    )

    answer = qa.run(query)
    return answer
