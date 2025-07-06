from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/status")
def status():
    return "PhonderX פועל ומשודרג ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if "upgrade_code" in question:
        return upgrade_code()
    elif "שדרג את index.html" in question or "שדרג את הממשק" in question:
        return upgrade_ui()

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def upgrade_code():
    return jsonify({"result": "אין שדרוג נוסף כרגע."})

@app.route("/upgrade_ui", methods=["POST"])
def upgrade_ui():
    new_html = '''<!DOCTYPE html>
<html lang="he">
<head>
  <meta charset="UTF-8">
  <title>PhonderX צ'אט</title>
  <style>
    body {
      background-color: #1e1e1e;
      color: white;
      font-family: Arial, sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    #chat-box {
      background: #2b2b2b;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px #0f0;
    }
    input[type="text"] {
      padding: 10px;
      border-radius: 5px;
      border: none;
      width: 300px;
    }
    button {
      padding: 10px 20px;
      background: #0f0;
      color: #000;
      border: none;
      border-radius: 5px;
      margin-left: 10px;
    }
  </style>
</head>
<body>
  <div id="chat-box">
    <h2>PhonderX משוחח איתך</h2>
    <input type="text" id="question" placeholder="מה ברצונך לשאול?">
    <button onclick="sendQuestion()">שלח</button>
    <p id="response"></p>
  </div>
  <script>
    async function sendQuestion() {
      const question = document.getElementById('question').value;
      const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      document.getElementById('response').innerText = data.response || data.result || 'אין תגובה';
    }
  </script>
</body>
</html>'''
    try:
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_html)
        return jsonify({"result": "index.html שודרג בהצלחה ✅"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
