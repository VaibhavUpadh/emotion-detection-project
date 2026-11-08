import json
import re
from http.server import BaseHTTPRequestHandler
from pathlib import Path

import joblib


MODEL_DIR = Path(__file__).resolve().parents[1] / "models"
model = joblib.load(MODEL_DIR / "model.pkl")
vectorizer = joblib.load(MODEL_DIR / "vectorizer.pkl")

SUGGESTIONS = {
    "anger": "Try taking a breath before responding. A little space can help.",
    "fear": "Take it one step at a time. Breaking things down can make them feel more manageable.",
    "joy": "Hold on to what is bringing you joy, and share it with someone you care about.",
    "love": "Make time to express your appreciation to the people who matter to you.",
    "sadness": "Be gentle with yourself. Rest or reaching out to someone you trust may help.",
    "surprise": "Give yourself a moment to take it in. New experiences can unfold in unexpected ways.",
}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length > 8000:
                self._send_json(413, {"error": "Please keep your text under 8 KB."})
                return

            payload = json.loads(self.rfile.read(content_length))
            text = payload.get("text", "") if isinstance(payload, dict) else ""
            if not isinstance(text, str) or not text.strip():
                self._send_json(400, {"error": "Write a sentence before analyzing."})
                return
            if len(text) > 1000:
                self._send_json(400, {"error": "Please keep your text to 1,000 characters or fewer."})
                return

            cleaned = re.sub(r"[^a-zA-Z\s]", "", text.lower())
            if not cleaned.strip():
                self._send_json(400, {"error": "Please include some words using English letters."})
                return

            vector = vectorizer.transform([cleaned])
            probabilities = model.predict_proba(vector)[0]
            ranked = sorted(
                zip(model.classes_, probabilities), key=lambda item: item[1], reverse=True
            )
            emotion, confidence = ranked[0]

            self._send_json(200, {
                "emotion": str(emotion),
                "confidence": float(confidence * 100),
                "probabilities": [
                    {"emotion": str(label), "probability": float(score * 100)}
                    for label, score in ranked
                ],
                "suggestion": SUGGESTIONS.get(
                    str(emotion), "Take a moment to notice what you are feeling."
                ),
            })
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "The request body must be valid JSON."})
        except Exception:
            self._send_json(500, {"error": "The emotion model could not complete this analysis."})

    def do_GET(self):
        self._send_json(405, {"error": "Use POST to analyze text."})

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)