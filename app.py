from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# ✅ Enable CORS properly
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return "Backend is running 🚀"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # ✅ Handle preflight request
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()

    # ✅ Safety check (prevents crash)
    if not data or "message" not in data:
        return jsonify({"reply": "No message received"}), 400

    user_message = data["message"]

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
        )

        result = response.json()

        # ✅ Safe parsing (no crash)
        reply = (
            result.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "No reply from AI")
        )

    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})