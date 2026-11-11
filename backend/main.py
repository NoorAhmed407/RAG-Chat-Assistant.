
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.embeddings import load_embedding_model
from src.vector_store import load_vector_store, load_chunks
from src.retriever import retrieve_documents
from src.generator import generate_answer


# Load resources once when the API starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_embedding_model()
    app.state.index = load_vector_store()
    app.state.chunks = load_chunks()

    yield


app = FastAPI(lifespan=lifespan)


# Allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG API is running!"}


@app.post("/chat")
def chat(request: ChatRequest):

    results = retrieve_documents(
        question=request.question,
        model=app.state.model,
        index=app.state.index,
        chunks=app.state.chunks,
        top_k=3,
        similarity_threshold=0.35
    )

    answer = generate_answer(
        request.question,
        results
    )

    sources = [
        {
            "source": result["source"],
            "page": result["page"],
            "score": round(result["score"], 4)
        }
        for result in results
    ]

    return {
        "answer": answer,
        "mode": "Knowledge Base" if results else "General Knowledge",
        "sources": sources
    }
