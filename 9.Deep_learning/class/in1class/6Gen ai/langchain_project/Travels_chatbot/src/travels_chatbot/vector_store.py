from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


def build_vector_store(
    documents: list[Document],
    embeddings: Embeddings,
    persist_directory: Path,
    collection_name: str,
    rebuild: bool = False,
) -> Chroma:
    persist_directory.mkdir(parents=True, exist_ok=True)
    ids = [document.metadata["chunk_id"] for document in documents]

    if rebuild:
        vectorstore = Chroma(
            collection_name=collection_name,
            persist_directory=str(persist_directory),
            embedding_function=embeddings,
        )
        vectorstore.reset_collection()
        vectorstore.add_documents(documents=documents, ids=ids)
        return vectorstore

    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        ids=ids,
        collection_name=collection_name,
        persist_directory=str(persist_directory),
    )


def load_vector_store(
    embeddings: Embeddings,
    persist_directory: Path,
    collection_name: str,
) -> Chroma:
    return Chroma(
        collection_name=collection_name,
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
    )
