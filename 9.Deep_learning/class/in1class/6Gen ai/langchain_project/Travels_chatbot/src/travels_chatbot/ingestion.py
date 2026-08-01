from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


@dataclass(frozen=True)
class PdfLoadReport:
    pdf_count: int
    page_count: int
    text_page_count: int
    empty_page_count: int
    chunks_count: int
    chunks_by_pdf: dict[str, int]
    pages_by_pdf: dict[str, int]


def load_pdf_pages(pdf_dir: Path) -> list[Document]:
    documents: list[Document] = []
    pdf_files = sorted(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {pdf_dir}")

    for pdf_path in pdf_files:
        with fitz.open(pdf_path) as pdf:
            for page_index, page in enumerate(pdf, start=1):
                text = page.get_text("text").strip()
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(pdf_path),
                            "source_name": pdf_path.name,
                            "page": page_index,
                            "total_pages": pdf.page_count,
                        },
                    )
                )

    return documents


def split_documents(
    pages: list[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    text_pages = [page for page in pages if page.page_content.strip()]
    chunks = splitter.split_documents(text_pages)

    for chunk_index, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = chunk_index
        chunk.metadata["chunk_id"] = make_chunk_id(chunk)
        chunk.page_content = f"Source PDF: {chunk.metadata['source_name']}\n{chunk.page_content}"

    return chunks


def make_chunk_id(document: Document) -> str:
    source_name = document.metadata["source_name"]
    page = document.metadata["page"]
    chunk_index = document.metadata.get("chunk_index", 0)
    return f"{source_name}::p{page}::c{chunk_index}"


def build_load_report(pages: list[Document], chunks: list[Document]) -> PdfLoadReport:
    pdf_names = {page.metadata["source_name"] for page in pages}
    pages_by_pdf: dict[str, int] = {}
    chunks_by_pdf: dict[str, int] = {}

    for page in pages:
        source_name = page.metadata["source_name"]
        pages_by_pdf[source_name] = pages_by_pdf.get(source_name, 0) + 1

    for chunk in chunks:
        source_name = chunk.metadata["source_name"]
        chunks_by_pdf[source_name] = chunks_by_pdf.get(source_name, 0) + 1

    text_page_count = sum(1 for page in pages if page.page_content.strip())
    return PdfLoadReport(
        pdf_count=len(pdf_names),
        page_count=len(pages),
        text_page_count=text_page_count,
        empty_page_count=len(pages) - text_page_count,
        chunks_count=len(chunks),
        chunks_by_pdf=chunks_by_pdf,
        pages_by_pdf=pages_by_pdf,
    )
