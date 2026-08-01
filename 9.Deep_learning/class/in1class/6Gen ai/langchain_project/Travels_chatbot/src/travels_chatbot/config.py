from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    pdf_dir: Path = PROJECT_ROOT / "pdfs"
    chroma_dir: Path = PROJECT_ROOT / "chroma_db"
    collection_name: str = "travel_pdf_rag"
    chunk_size: int = 900
    chunk_overlap: int = 150
    retriever_k: int = 5
    embedding_provider: str = "hash"
    llm_provider: str = "groq"
    llm_model: str = "llama-3.1-8b-instant"


def load_settings() -> Settings:
    load_dotenv(PROJECT_ROOT / ".env")

    return Settings(
        pdf_dir=Path(os.getenv("PDF_DIR", PROJECT_ROOT / "pdfs")),
        chroma_dir=Path(os.getenv("CHROMA_DIR", PROJECT_ROOT / "chroma_db")),
        collection_name=os.getenv("CHROMA_COLLECTION", "travel_pdf_rag"),
        chunk_size=int(os.getenv("CHUNK_SIZE", "900")),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "150")),
        retriever_k=int(os.getenv("RETRIEVER_K", "5")),
        embedding_provider=os.getenv("RAG_EMBEDDING_PROVIDER", "hash").lower(),
        llm_provider=os.getenv("RAG_LLM_PROVIDER", "groq").lower(),
        llm_model=os.getenv("RAG_LLM_MODEL", "llama-3.1-8b-instant"),
    )

