from __future__ import annotations

import argparse
from dataclasses import dataclass

from src.travels_chatbot.config import load_settings
from src.travels_chatbot.embeddings import build_embeddings
from src.travels_chatbot.evaluation import build_source_queries, evaluate_retrieval
from src.travels_chatbot.ingestion import build_load_report, load_pdf_pages, split_documents
from src.travels_chatbot.rag_chain import build_llm, build_rag_chain
from src.travels_chatbot.vector_store import build_vector_store, load_vector_store


@dataclass
class FeedbackStats:
    total: int = 0
    correct: int = 0

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total else 0.0


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiment with PDF RAG ingestion and retrieval.")
    parser.add_argument("--ask", help="Ask one question after the vector DB is built.")
    parser.add_argument("--chat", action="store_true", help="Start an interactive travel bot loop.")
    parser.add_argument("--no-rebuild", action="store_true", help="Reuse the existing Chroma directory.")
    parser.add_argument("--no-llm", action="store_true", help="Skip answer generation and only test retrieval.")
    args = parser.parse_args()

    settings = load_settings()
    embeddings = build_embeddings(settings.embedding_provider)

    pages = load_pdf_pages(settings.pdf_dir)
    chunks = split_documents(pages, settings.chunk_size, settings.chunk_overlap)
    load_report = build_load_report(pages, chunks)

    if args.no_rebuild:
        vectorstore = load_vector_store(
            embeddings=embeddings,
            persist_directory=settings.chroma_dir,
            collection_name=settings.collection_name,
        )
    else:
        vectorstore = build_vector_store(
            documents=chunks,
            embeddings=embeddings,
            persist_directory=settings.chroma_dir,
            collection_name=settings.collection_name,
            rebuild=True,
        )

    collection_count = vectorstore._collection.count()
    queries = build_source_queries(chunks)
    eval_report = evaluate_retrieval(vectorstore, queries, k=settings.retriever_k)

    print("\nPDF INGESTION COVERAGE")
    print(f"PDF files loaded       : {load_report.pdf_count}")
    print(f"Pages loaded           : {load_report.page_count}")
    print(f"Pages with text        : {load_report.text_page_count}")
    print(f"Empty/scanned pages    : {load_report.empty_page_count}")
    print(f"Chunks created         : {load_report.chunks_count}")
    print(f"Chunks stored in Chroma: {collection_count}")
    print(f"Embedding provider     : {settings.embedding_provider}")

    print("\nPDF CHUNK COVERAGE")
    missing_chunks = []
    for pdf_name in sorted(load_report.pages_by_pdf):
        chunk_count = load_report.chunks_by_pdf.get(pdf_name, 0)
        if chunk_count == 0:
            missing_chunks.append(pdf_name)
        print(f"- {pdf_name}: pages={load_report.pages_by_pdf[pdf_name]}, chunks={chunk_count}")

    print("\nRETRIEVAL ACCURACY EXPERIMENT")
    print(f"Queries tested : {eval_report.total_queries}")
    print(f"Top-{settings.retriever_k} hits: {eval_report.hits}")
    print(f"Hit rate       : {eval_report.hit_rate:.2%}")

    failed = [result for result in eval_report.results if not result.hit]
    if failed:
        print("\nMissed queries")
        for result in failed:
            print(f"- expected={result.expected_source} | query={result.query}")
            print(f"  retrieved={result.top_sources}")

    if missing_chunks:
        raise SystemExit(f"\nSome PDFs produced zero chunks: {missing_chunks}")
    if collection_count != load_report.chunks_count:
        raise SystemExit(
            f"\nChroma count mismatch: stored={collection_count}, expected={load_report.chunks_count}"
        )

    if args.ask and not args.no_llm:
        llm = build_llm(settings.llm_provider, settings.llm_model)
        retriever = vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k})
        rag_chain = build_rag_chain(retriever, llm)
        print("\nRAG ANSWER")
        print(rag_chain.invoke(args.ask))
    elif args.ask:
        print("\nTop retrieved chunks")
        docs = vectorstore.similarity_search(args.ask, k=settings.retriever_k)
        for doc in docs:
            print(f"- {doc.metadata['source_name']} page {doc.metadata['page']}")

    if args.chat:
        run_chat_loop(vectorstore, settings, no_llm=args.no_llm)


def run_chat_loop(vectorstore, settings, no_llm: bool) -> None:
    stats = FeedbackStats()
    rag_chain = None

    if not no_llm:
        llm = build_llm(settings.llm_provider, settings.llm_model)
        retriever = vectorstore.as_retriever(search_kwargs={"k": settings.retriever_k})
        rag_chain = build_rag_chain(retriever, llm)

    print("\nTRAVEL BOT CHAT")
    print("Ask travel questions from the PDFs. Type 'exit', 'quit', or 'q' to stop.")

    while True:
        question = input("\nYour question: ").strip()
        if question.lower() in {"exit", "quit", "q"}:
            break
        if not question:
            continue

        if rag_chain is None:
            print("\nTop retrieved PDF chunks")
            docs = vectorstore.similarity_search(question, k=settings.retriever_k)
            for index, doc in enumerate(docs, start=1):
                source = doc.metadata.get("source_name", "unknown")
                page = doc.metadata.get("page", "unknown")
                preview = " ".join(doc.page_content.split())[:300]
                print(f"{index}. {source} page {page}")
                print(f"   {preview}")
        else:
            print("\nTravel bot answer")
            print(rag_chain.invoke(question))

            print("\nSources")
            docs = vectorstore.similarity_search(question, k=settings.retriever_k)
            for doc in docs:
                source = doc.metadata.get("source_name", "unknown")
                page = doc.metadata.get("page", "unknown")
                print(f"- {source} page {page}")

        feedback = input("\nWas this answer correct? (y/n/skip): ").strip().lower()
        if feedback in {"y", "yes"}:
            stats.total += 1
            stats.correct += 1
        elif feedback in {"n", "no"}:
            stats.total += 1

    print("\nCHAT FEEDBACK SUMMARY")
    print(f"Rated answers : {stats.total}")
    print(f"Correct       : {stats.correct}")
    print(f"Accuracy      : {stats.accuracy:.2%}")


if __name__ == "__main__":
    main()


# demo.py --chat --no-llm