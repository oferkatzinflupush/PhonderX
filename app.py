from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
