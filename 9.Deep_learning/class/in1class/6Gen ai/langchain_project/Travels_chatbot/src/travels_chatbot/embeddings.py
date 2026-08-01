from __future__ import annotations

import hashlib
import math
import re
from collections import Counter
from typing import Iterable

from langchain_core.embeddings import Embeddings


TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")


class HashEmbeddings(Embeddings):
    """Deterministic local embeddings for offline ingestion and retrieval tests."""

    def __init__(self, dimensions: int = 768) -> None:
        self.dimensions = dimensions

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        counts = Counter(self._tokens(text))

        for token, count in counts.items():
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            bucket = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[bucket] += sign * (1.0 + math.log(count))

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector
        return [value / norm for value in vector]

    @staticmethod
    def _tokens(text: str) -> Iterable[str]:
        return (match.group(0).lower() for match in TOKEN_RE.finditer(text))


def build_embeddings(provider: str) -> Embeddings:
    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model="text-embedding-3-small")

    if provider == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    if provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if provider == "hash":
        return HashEmbeddings()

    raise ValueError(
        "Unsupported RAG_EMBEDDING_PROVIDER. Use one of: hash, openai, google, huggingface."
    )

