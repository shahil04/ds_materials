from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from langchain_core.documents import Document


STOPWORDS = {
    "pdf",
    "itinerary",
    "brochure",
    "destino",
    "new",
    "with",
    "via",
    "days",
    "night",
}


@dataclass(frozen=True)
class RetrievalResult:
    query: str
    expected_source: str
    top_sources: list[str]
    hit: bool


@dataclass(frozen=True)
class EvaluationReport:
    total_queries: int
    hits: int
    hit_rate: float
    results: list[RetrievalResult]


def build_source_queries(chunks: list[Document]) -> list[tuple[str, str]]:
    first_chunk_by_source: dict[str, Document] = {}
    for chunk in chunks:
        source_name = chunk.metadata["source_name"]
        first_chunk_by_source.setdefault(source_name, chunk)

    queries: list[tuple[str, str]] = []
    for source_name, chunk in sorted(first_chunk_by_source.items()):
        stem_words = _keywords(Path(source_name).stem)
        chunk_words = _keywords(chunk.page_content)[:6]
        query = " ".join(stem_words[:8] + chunk_words)
        if not query.strip():
            query = Path(source_name).stem
        queries.append((query, source_name))
    return queries


def evaluate_retrieval(vectorstore, queries: list[tuple[str, str]], k: int = 5) -> EvaluationReport:
    results: list[RetrievalResult] = []
    for query, expected_source in queries:
        docs = vectorstore.similarity_search(query, k=k)
        top_sources = [doc.metadata.get("source_name", "") for doc in docs]
        results.append(
            RetrievalResult(
                query=query,
                expected_source=expected_source,
                top_sources=top_sources,
                hit=expected_source in top_sources,
            )
        )

    hits = sum(1 for result in results if result.hit)
    total = len(results)
    return EvaluationReport(
        total_queries=total,
        hits=hits,
        hit_rate=hits / total if total else 0.0,
        results=results,
    )


def _keywords(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9]+", text.lower())
    unique: list[str] = []
    for word in words:
        if word in STOPWORDS or len(word) < 3 or word in unique:
            continue
        unique.append(word)
    return unique

