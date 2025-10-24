# Backend (Flask) for MCP-like app using Hugging Face models

## Requirements
- Python 3.8+
- pip

## Setup
```
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```
python app.py
```
The API will be available at http://localhost:7860/api/analyze

## Endpoint
POST /api/analyze
JSON body:
{
  "text": "your text here",
  "mode": null | "summary" | "sentiment" | "keywords" | "all"
}

Response JSON contains `summary`, `sentiment`, and/or `keywords` depending on router decision.
