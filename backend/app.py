from flask import Flask, request, jsonify
from flask_cors import CORS
from keybert import KeyBERT
from transformers import pipeline
import os

app = Flask(__name__)
CORS(app)

# Initialize Hugging Face pipelines and KeyBERT (uses sentence-transformers under the hood)
# Models can be changed via environment variables
SUMMARIZER_MODEL = os.environ.get("SUMMARIZER_MODEL", "facebook/bart-large-cnn")
SENTIMENT_MODEL = os.environ.get("SENTIMENT_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

summarizer = pipeline("summarization", model=SUMMARIZER_MODEL)
sentiment = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)
kw_model = KeyBERT(model=EMBEDDING_MODEL)

def router_decide(text, explicit_mode=None):
    """Decide which channels to run.
    explicit_mode: 'summary' | 'sentiment' | 'keywords' | 'all' | None
    If None -> heuristic:
      - if len(text) > 300 -> summary + keywords
      - if len(text) < 80 -> sentiment + keywords
      - otherwise -> keywords + summary
    """
    if explicit_mode in {"summary","sentiment","keywords","all"}:
        return explicit_mode
    n = len(text)
    if n > 600:
        return "summary"
    if n < 80:
        return "sentiment"
    return "keywords"

@app.route('/api/analyze', methods=['POST'])
def analyze():
    payload = request.get_json(force=True)
    text = payload.get("text", "")
    mode = payload.get("mode")  # optional explicit mode
    if not text:
        return jsonify({"error":"no text provided"}), 400

    decision = router_decide(text, explicit_mode=mode)
    result = {"decision": decision}

    try:
        if decision in ("summary","all","keywords"):
            # Summarize (if text is very short, summarizer may echo; we guard)
            if len(text) > 20:
                summ = summarizer(text, max_length=150, min_length=30, do_sample=False)
                result["summary"] = summ[0]["summary_text"]
            else:
                result["summary"] = text

        if decision in ("sentiment","all","keywords"):
            sent = sentiment(text[:1000])  # limit tokens
            # pipeline returns [{'label':'POSITIVE','score':0.99}]
            result["sentiment"] = sent[0]

        if decision in ("keywords","all","summary"):
            # extract keywords using KeyBERT (returns list of tuples)
            kws = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words='english', top_n=10)
            result["keywords"] = [k for k,score in kws]

    except Exception as e:
        return jsonify({"error":"processing failed","details":str(e)}), 500

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=True)
