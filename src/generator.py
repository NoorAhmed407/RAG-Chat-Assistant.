import ollama

MODEL_NAME = "qwen2.5:3b"


def generate_answer(question, retrieved_chunks):

    if retrieved_chunks:

        context = ""

        for i, chunk in enumerate(retrieved_chunks, start=1):
            context += f"""
            Context {i}
            Source: {chunk['source']}
            Page: {chunk['page']}
            Content: {chunk['text']}
            """

        prompt = f"""
        Answer the user's question using the provided documents.

        You may use your general knowledge to clarify the explanation,
        but prioritize the documents.

        If you introduce information not found in the documents,
        clearly distinguish it from document-based information.

        Context:
        {context}

        Question: {question}

        Answer:
        """

    else:

        prompt = f"""
        The user's question could not be answered using the available
        documents.

        Answer using your general pretrained knowledge instead.

        Be honest if you are uncertain. Do not claim that your answer
        comes from the documents.

        Question: {question}

        Answer:
        """

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]