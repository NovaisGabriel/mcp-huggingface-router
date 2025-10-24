# MCP-like project (Hugging Face)

This project is a self-contained example similar in spirit to https://github.com/NovaisGabriel/mcp-langchain
but using Hugging Face models (transformers + KeyBERT) instead of OpenAI/LangChain.

## Structure
- backend/: Flask API that uses Hugging Face pipelines and KeyBERT for summarization, sentiment analysis and keyword extraction.
- frontend/: Vite + React demo UI that POSTs text to the backend and displays results.

## Quick start (development)
1. Start backend:
   - cd backend
   - python -m venv .venv
   - source .venv/bin/activate
   - pip install -r requirements.txt
   - python app.py

2. Start frontend:
   - cd frontend
   - npm install
   - npm run dev

3. Open browser to the Vite dev server (usually http://localhost:5173) and submit text.

## Tests (backend)
In the backend virtualenv:
```
pytest -v
```
The tests mock the heavy ML calls so they run quickly.
