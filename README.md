# 🧠 MCP-HF: Multi-Capability Processor using Hugging Face

## 📘 Overview
**MCP-HF** (Multi-Capability Processor using Hugging Face) is a full-stack demo project inspired by [NovaisGabriel/mcp-langchain](https://github.com/NovaisGabriel/mcp-langchain).  
It demonstrates how to build a small modular system capable of analyzing text through multiple NLP tasks — all orchestrated by a simple router layer.

The backend (Flask + Hugging Face) automatically decides which task(s) to run — summarization, sentiment analysis, or keyword extraction — depending on the input text or user-selected mode.  
The frontend (React + Vite) provides a clean UI to input text and view the results.

---

## ⚙️ Features
- 🧩 **Router Layer**: Automatically routes the request based on text length or explicit mode.
- ✂️ **Summarization**: Uses `facebook/bart-large-cnn` to generate concise summaries.
- 💬 **Sentiment Analysis**: Uses `distilbert-base-uncased-finetuned-sst-2-english` for polarity detection.
- 🪄 **Keyword Extraction**: Uses `KeyBERT` with `sentence-transformers/all-MiniLM-L6-v2` for key terms.
- ⚡ **Modular & Extensible**: Easily plug in other Hugging Face models or tasks.
- 🧪 **Backend Tests**: Includes pytest tests with mocked ML models for fast local testing.

---

## 🧱 Project Structure
```
mcp-hf-project/
│
├── backend/                 # Flask API
│   ├── app.py               # Main API logic
│   ├── requirements.txt     # Dependencies
│   ├── tests/               # Unit tests with pytest
│   └── README.md
│
├── frontend/                # React + Vite app
│   ├── src/
│   │   ├── App.jsx          # Main component
│   │   └── main.jsx         # Entry point
│   ├── package.json
│   └── README.md
│
└── README.md                # (this file)
```

---

## 🚀 Getting Started

### 🧩 1. Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate.ps1
pip install -r requirements.txt
python app.py
```

API will run at: **http://localhost:7860/api/analyze**

### 🧠 Example API Request
**POST /api/analyze**
```json
{
  "text": "Artificial intelligence is transforming industries around the world.",
  "mode": "keywords"
}
```

**Response Example**
```json
{
  "decision": "keywords",
  "keywords": ["artificial intelligence", "industries", "transforming"]
}
```

---

### 💻 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Then open the Vite dev server (usually [http://localhost:5173](http://localhost:5173)).

Paste some text, choose the mode (`auto`, `summary`, `sentiment`, `keywords`, `all`), and click **Analyze**.

---

## 🧪 3. Running Tests
All backend tests are located in `backend/tests`.

They mock heavy ML models for quick testing:
```bash
cd backend
pytest -v
```

Expected output:
```
test_api.py::test_analyze_keywords PASSED
test_api.py::test_analyze_summary PASSED
```

---

## ⚡ Customization
You can switch to other Hugging Face models by setting environment variables before running the backend:
```bash
export SUMMARIZER_MODEL="google/pegasus-xsum"
export SENTIMENT_MODEL="nlptown/bert-base-multilingual-uncased-sentiment"
export EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2"
```
Then restart the Flask server.

---

## 🧰 Tech Stack
**Backend:**
- Flask + Flask-CORS  
- Hugging Face Transformers  
- KeyBERT + Sentence-Transformers  
- Pytest

**Frontend:**
- React + Vite  
- Axios for API calls

---

## 🧩 Architecture Summary
The backend mimics a lightweight “MCP router”:
1. **Router** inspects text (or explicit mode).
2. Routes to one or more processing “capabilities.”
3. **Summarizer**, **Sentiment Analyzer**, and **Keyword Extractor** produce results.
4. Combined response is sent to the frontend.

This modularity makes it easy to add new capabilities — e.g., translation, entity recognition, or topic classification.

---
