# API

The HTTP API is a FastAPI app in `backend/main.py`. On startup it loads the embedding model, `vector_store/index.faiss`, and `vector_store/chunks.json` once, then reuses them for every request.

```bash
uvicorn backend.main:app --reload
```

The server listens on `http://127.0.0.1:8000`.

Run ingestion first. The API does not read PDFs itself.

## Endpoints

`GET /` checks that the process is up.

```json
{ "message": "RAG API is running!" }
```

`POST /chat` answers one question. The body is:

```json
{ "question": "What is machine learning?" }
```

The response is:

```json
{
  "answer": "…",
  "sources": [
    { "source": "paper.pdf", "page": 4, "score": 0.4143 }
  ]
}
```

The API retrieves the top 3 chunks (`src/retriever.py`), then `src/generator.py` sends those chunks and the question to Ollama (`qwen2.5:3b`). If nothing is retrieved, the answer is `I couldn't find relevant information.` and `sources` is empty.

The browser origins allowed by CORS are `http://localhost:5173` and `http://127.0.0.1:5173`.
