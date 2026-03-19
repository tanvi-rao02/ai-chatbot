from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Enable CORS for all domains (important for Vercel)
CORS(app)

# ✅ Health check route (optional but useful)
@app.route("/")
def home():
    return "Backend is running 🚀"

# ✅ Chat route
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # ✅ Handle preflight request (VERY IMPORTANT for CORS)
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})

    user_message = request.json.get("message")

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
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant for students. Explain in simple words."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        data = response.json()

        # ✅ Safe handling
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = "Error: " + data["error"]["message"]
        else:
            reply = "Unexpected response"

    except Exception as e:
        reply = "Error: " + str(e)

    return jsonify({"reply": reply})


# ✅ Run server properly on Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)