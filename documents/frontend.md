# Frontend

`frontend/` is a React app built with Vite. It is a single chat page that sends each question to the API.

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The API must already be running at `http://127.0.0.1:8000`.

## Request

The page posts to `http://127.0.0.1:8000/chat`:

```json
{ "question": "your question" }
```

It shows the `answer` text, then each item in `sources` as the filename, page, and similarity score. The input stays disabled while a request is in progress.

`npm run build` writes a production bundle to `frontend/dist/`. That folder and `frontend/node_modules/` are gitignored.
