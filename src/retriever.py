from src.vector_store import search_vectors


def retrieve_documents(
    question,
    model,
    index,
    chunks,
    top_k=3,
    similarity_threshold=0.35
):

    query_embedding = model.encode(
        [question],
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    scores, indices = search_vectors(
        query_embedding,
        index,
        top_k
    )

    results = []

    for score, idx in zip(scores, indices):

        if idx == -1:
            continue

        if score < similarity_threshold:
            continue

        result = chunks[int(idx)].copy()
        result["score"] = float(score)

        results.append(result)

    return results