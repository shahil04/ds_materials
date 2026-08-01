from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


SYSTEM_PROMPT = """You are a travel itinerary assistant.
Answer only from the provided PDF context.
If the answer is not present in the context, say that the PDFs do not contain it.
For location questions, use itinerary places, sightseeing stops, destinations, pickup points,
and route details from the context.
Mention the package/destination, include source PDF/page citations, and keep the answer concise."""


def format_docs(docs) -> str:
    formatted = []
    for doc in docs:
        source_name = doc.metadata.get("source_name", "unknown")
        page = doc.metadata.get("page", "unknown")
        formatted.append(f"[{source_name}, page {page}]\n{doc.page_content}")
    return "\n\n".join(formatted)


def build_llm(provider: str, model: str):
    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(model=model, temperature=0)

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model, temperature=0)

    if provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=model, temperature=0)

    raise ValueError("Unsupported RAG_LLM_PROVIDER. Use one of: groq, openai, google.")


def build_rag_chain(retriever, llm):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "Question: {question}\n\nContext:\n{context}"),
        ]
    )

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
