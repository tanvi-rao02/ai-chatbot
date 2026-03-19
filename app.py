from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ✅ FORCE CORS HEADERS (FIXES YOUR ISSUE)
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


@app.route("/")
def home():
    return "Backend is running 🚀"


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # ✅ HANDLE PREFLIGHT (THIS IS THE KEY FIX)
    if request.method == "OPTIONS":
        return "", 200

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
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": user_message}
                ]
            }
        )

        data = response.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = str(data)

    except Exception as e:
        reply = str(e)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 