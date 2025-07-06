from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PhonderX is alive and online."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    return jsonify({"response": f"PhonderX קיבל את השאלה: {question} (תשובה אמיתית תיכנס כאן)"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
