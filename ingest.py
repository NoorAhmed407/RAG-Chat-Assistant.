from src.loader import load_all_pdfs
from src.chunker import clean_text, chunk_text
from src.embeddings import load_embedding_model, generate_embeddings
from src.vector_store import create_vector_store, save_vector_store, save_chunks


def ingest(data_dir="data", chunk_size=500, overlap=50):
    documents = load_all_pdfs(data_dir)

    all_chunks = []

    for document in documents:
        cleaned_text = clean_text(document["text"])

        chunks = chunk_text(
            cleaned_text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for index, chunk in enumerate(chunks):
            all_chunks.append({
                "source": document["source"],
                "page": document["page"],
                "chunk_id": index,
                "text": chunk
            })

    model = load_embedding_model()

    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = generate_embeddings(texts, model)

    index = create_vector_store(embeddings)

    save_vector_store(index)
    save_chunks(all_chunks)

    print(f"Ingested {len(all_chunks)} chunks from {len(documents)} pages")


if __name__ == "__main__":
    ingest()
