from dotenv import load_dotenv
load_dotenv()   # ✅ FIXED

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return "AI Chatbot is running"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant for students. Explain in simple words with examples."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        data = response.json()
        print("FULL API RESPONSE:", data)

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = "Error: " + data["error"]["message"]
        else:
            reply = "Unexpected response"

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"reply": reply})


# ✅ FINAL RUN BLOCK (VERY IMPORTANT FOR RENDER)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    print("Starting server on port:", port)
    app.run(host="0.0.0.0", port=port, debug=False)