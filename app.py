from dotenv import load_dotenv 
load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔑 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
import os
API_KEY = os.getenv"API_KEY"

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
                # ✅ Stable working model
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

        # ✅ Safe response handling
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = "Error: " + data["error"]["message"]
        else:
            reply = "Unexpected response"

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)