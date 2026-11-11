from src.embeddings import load_embedding_model
from src.vector_store import load_vector_store, load_chunks
from src.retriever import retrieve_documents
from src.generator import generate_answer


# Loaded once for this process. The files on disk stay as ingest.py wrote them.
model = load_embedding_model()
index = load_vector_store()
chunks = load_chunks()

print("Ready. Ask a question, or press Enter to quit.")

while True:
    question = input("\nQuestion: ").strip()

    if not question:
        break

    results = retrieve_documents(
        question=question,
        model=model,
        index=index,
        chunks=chunks,
        top_k=2
    )
   
    # Generate answer using local LLM
    answer = generate_answer(question, results)

    print("\n========== ANSWER ==========")
    print(answer)

    print("\n========== SOURCES ==========")

    if len(results):
        for result in results:
            print(f"{result['source']} - Page {result['page']}")
    else:
        print("General Knowledge")
    