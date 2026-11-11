# RAG pipeline

This project answers questions from local PDFs. It loads the files, splits them into chunks, stores embeddings in FAISS, retrieves the closest chunks, and asks a local Ollama model to answer from that context.

## Pieces

| Step | Where | What it does |
| --- | --- | --- |
| Ingestion | `ingest.py` | Reads `data/*.pdf` and writes `vector_store/` |
| Command-line chat | `main.py` | Loads the saved index and answers questions in the terminal |
| API | `backend/main.py` | Same retrieval and answer, over HTTP |
| UI | `frontend/` | React page that posts questions to the API |

More detail:

- [Ingestion](ingestion.md)
- [API](api.md)
- [Frontend](frontend.md)

## Setup

Python dependencies are listed in `requirements.txt`. The virtual environment used locally is `rag-env` and is not committed.

```bash
python -m venv rag-env
source rag-env/bin/activate
pip install -r requirements.txt
```

Answers are generated with Ollama using `qwen2.5:3b` (`src/generator.py`). Ollama needs to be running with that model installed before you ask a question.

```bash
ollama pull qwen2.5:3b
```

## Typical order

1. Put PDFs in `data/`.
2. Run `python ingest.py`.
3. Ask from the terminal with `python main.py`, or start the API and the React app.
