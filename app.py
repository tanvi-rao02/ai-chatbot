from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ✅ GLOBAL CORS HEADERS (for every request)
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response


# ✅ TEST ROUTE
@app.route("/")
def home():
    return "Backend is running 🚀"


# ✅ CHAT ROUTE (FIXED CORS + OPTIONS)
@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():

    # 🔥 HANDLE PREFLIGHT REQUEST (VERY IMPORTANT)
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

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

        # ✅ SAFE RESPONSE HANDLING
        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        elif "error" in data:
            reply = "Error: " + data["error"]["message"]
        else:
            reply = "Unexpected response"

    except Exception as e:
        reply = "Error: " + str(e)

    response = jsonify({"reply": reply})

    # ✅ EXTRA SAFETY HEADER
    response.headers["Access-Control-Allow-Origin"] = "*"

    return response


# ✅ RUN SERVER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)