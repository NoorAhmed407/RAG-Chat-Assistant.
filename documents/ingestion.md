# Ingestion

`ingest.py` builds the search index. Run it again whenever the PDFs in `data/` change.

```bash
python ingest.py
```

## What it does

1. `src/loader.py` reads every PDF in `data/` and keeps the filename, page number, and page text.
2. `src/chunker.py` cleans the text and splits it into chunks of 500 words with an overlap of 50 words.
3. `src/embeddings.py` embeds each chunk with `sentence-transformers/all-MiniLM-L6-v2`. Embeddings are normalized.
4. `src/vector_store.py` stores the vectors in a FAISS inner-product index and writes two files:
   - `vector_store/index.faiss`
   - `vector_store/chunks.json`

`chunks.json` keeps the text that belongs to each vector, plus `source`, `page`, and `chunk_id`. Retrieval uses that file to turn a FAISS hit back into a passage.

The model, index, and chunks are loaded once when you start `main.py` or the API. They are not rebuilt on each question.
