import json
import os
import faiss
import numpy as np


def create_vector_store(embeddings):
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    embeddings = np.asarray(embeddings, dtype=np.float32)

    index.add(embeddings)

    return index


def save_vector_store(index, path="vector_store/index.faiss"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    faiss.write_index(index, path)

    print(f"Vector store saved to {path}")


def load_vector_store(path="vector_store/index.faiss"):
    return faiss.read_index(path)


def search_vectors(query_embedding, index, top_k=3):
    query_embedding = np.asarray(query_embedding, dtype=np.float32)
    query_embedding = query_embedding.reshape(1, -1)

    scores, indices = index.search(query_embedding, top_k)

    return scores[0], indices[0]


# Chunk metadata storage

def save_chunks(chunks, path="vector_store/chunks.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)

    print(f"Chunks saved to {path}")


def load_chunks(path="vector_store/chunks.json"):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)