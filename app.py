from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)

# ✅ FORCE CORS HARD (VERY IMPORTANT)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def home():
    return "Backend is running 🚀"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # ✅ HANDLE PREFLIGHT REQUEST (THIS FIXES YOUR ERROR)
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    user_message = data.get("message")

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
        reply = result.get("choices", [{}])[0].get("message", {}).get("content", "No reply")

    except Exception as e:
        reply = str(e)

    return jsonify({"reply": reply})