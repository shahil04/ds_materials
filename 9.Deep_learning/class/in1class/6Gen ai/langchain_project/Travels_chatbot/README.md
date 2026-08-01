# Travels Chatbot RAG

Production-style RAG scaffold for travel itinerary PDFs.

## Folder Structure

- `pdfs/` - source travel package PDFs.
- `src/travels_chatbot/config.py` - environment-driven settings.
- `src/travels_chatbot/ingestion.py` - PDF page extraction and chunking.
- `src/travels_chatbot/embeddings.py` - OpenAI, Google, HuggingFace, or offline hash embeddings.
- `src/travels_chatbot/vector_store.py` - Chroma build/load helpers.
- `src/travels_chatbot/rag_chain.py` - retrieval augmented chatbot chain.
- `src/travels_chatbot/evaluation.py` - PDF coverage and retrieval accuracy experiment helpers.
- `demo.py` - first experiment entry point.

## Run The Demo

```powershell
.\.venv\Scripts\python.exe demo.py --no-llm
```

This loads every PDF, chunks text pages, embeds all chunks, stores them in Chroma,
then reports:

- number of PDFs/pages/chunks loaded
- chunks per PDF
- Chroma stored chunk count
- top-k retrieval hit rate by source PDF

Ask a retrieval-only question:

```powershell
.\.venv\Scripts\python.exe demo.py --no-llm --ask "What is included in the Shimla package?"
```

Ask with an LLM answer:

```powershell
.\.venv\Scripts\python.exe demo.py --ask "What is included in the Shimla package?"
```

Start the interactive travel bot loop:

```powershell
.\.venv\Scripts\python.exe demo.py --chat
```

Run the interactive loop without LLM API calls:

```powershell
.\.venv\Scripts\python.exe demo.py --chat --no-llm
```

After each question, the demo asks whether the answer was correct and prints a
feedback accuracy summary when you exit.

## Production Settings

Copy `.env.example` values into `.env` and choose providers:

- `RAG_EMBEDDING_PROVIDER=hash` for offline experiments.
- `RAG_EMBEDDING_PROVIDER=openai` for `text-embedding-3-small`.
- `RAG_EMBEDDING_PROVIDER=google` for `models/embedding-001`.
- `RAG_EMBEDDING_PROVIDER=huggingface` for local sentence-transformer embeddings.

For production chatbot accuracy, prefer OpenAI, Google, or HuggingFace semantic
embeddings over the offline hash baseline.
