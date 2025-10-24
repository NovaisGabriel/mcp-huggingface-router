import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

class DummyPipeline:
    def __init__(self, kind=None):
        self.kind = kind
    def __call__(self, text, **kwargs):
        if self.kind == "summarization":
            return [{"summary_text": "SHORT SUMMARY"}]
        if self.kind == "sentiment":
            return [{"label":"POSITIVE","score":0.99}]
        return []

class DummyKeyBert:
    def extract_keywords(self, text, **kwargs):
        return [("keyword1", 0.9), ("keyword2", 0.8)]

@pytest.fixture(autouse=True)
def patch_pipelines(monkeypatch):
    # Monkeypatch the pipelines and KeyBERT in the imported app module
    import app as appmod
    monkeypatch.setattr(appmod, "summarizer", DummyPipeline("summarization"))
    monkeypatch.setattr(appmod, "sentiment", DummyPipeline("sentiment"))
    monkeypatch.setattr(appmod, "kw_model", DummyKeyBert())

def test_analyze_keywords(client):
    c = client
    # Make text longer than 80 chars so router picks 'keywords'
    text = "This is a test paragraph about Python, Flask, and Hugging Face. " * 3
    r = c.post("/api/analyze", json={"text": text})
    data = r.get_json()
    assert r.status_code == 200
    assert "keywords" in data
    assert data["keywords"][0] == "keyword1"

def test_analyze_summary(client):
    c = app.test_client()
    long_text = "Long text " * 200
    r = c.post("/api/analyze", json={"text":long_text})
    assert r.status_code == 200
    data = r.get_json()
    assert "summary" in data
    assert data["summary"] == "SHORT SUMMARY"
