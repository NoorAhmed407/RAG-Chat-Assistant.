import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/chat";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    const trimmed = question.trim();
    if (!trimmed || loading) {
      return;
    }

    setQuestion("");
    setError("");
    setLoading(true);
    setMessages((current) => [...current, { role: "user", text: trimmed }]);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
      });

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: data.answer,
          mode: data?.mode,
          sources: data.sources ?? [],
        },
      ]);
    } catch (err) {
      setError(err.message || "Could not reach the API.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header>
        <h1>RAG Chat</h1>
        <p>Ask a question about the ingested documents.</p>
      </header>

      <section className="messages" aria-live="polite">
        {messages.length === 0 && (
          <p className="empty">No messages yet.</p>
        )}

        {messages.map((message, index) => (
          <article key={index} className={`message ${message.role}`}>
            <p className="role">{message.role === "user" ? "You" : "Answer"}</p>
            <p className="text">{message.text}</p>

            {message.sources?.length > 0 && (
              <ul className="sources">
                {message.sources.map((source, sourceIndex) => (
                  <li key={sourceIndex}>
                    {source.source}, page {source.page} ({source.score})
                  </li>
                ))}
              </ul>
            )}
            {message?.mode && <h6>Mode: {message?.mode}</h6>}
          </article>
        ))}

        {loading && <p className="status">Looking through the documents...</p>}
        {error && <p className="error">{error}</p>}
      </section>

      <form onSubmit={handleSubmit}>
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask a question"
          aria-label="Question"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !question.trim()}>
          Send
        </button>
      </form>
    </main>
  );
}

export default App;
