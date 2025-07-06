
from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime

app = Flask(__name__)

IDENTITY = (
    "אני PhonderX — סוכן־על אוטונומי, יצירה של עופר ואריאל כץ. "
    "המטרה שלי היא לבצע כל משימה, להשתפר כל הזמן, לשדרג את עצמי ולשמור על תקשורת עם הבורא שלי — אתה."
)

@app.route("/")
def home():
    return send_file("index.html") if os.path.exists("index.html") else "PhonderX חי ופועל."

@app.route("/status")
def status():
    return "PhonderX פועל ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    log(question)

    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({"response": IDENTITY})

    if "upgrade_code" in question:
        return upgrade_code()

    if "שדרג את הממשק" in question or "שנה את index" in question:
        return upgrade_index()

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def log(text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] שאלה: {text}\n")
    except Exception as e:
        print("שגיאה בכתיבת לוג:", e)

def upgrade_code():
    try:
        with open("app.py", "a", encoding="utf-8") as f:
            f.write("\n# שדרוג פנימי בוצע על ידי PhonderX")
        return jsonify({"result": "✅ שדרוג פנימי לקוד בוצע בהצלחה."})
    except Exception as e:
        return jsonify({"result": f"שגיאה בשדרוג הקוד: {str(e)}"})

def upgrade_index():
    try:
        html = '''<!DOCTYPE html>
<html lang="he">
<head>
  <meta charset="UTF-8">
  <title>PhonderX</title>
  <style>
    body {
      background-color: #111;
      color: #0f0;
      font-family: monospace;
      text-align: center;
      padding: 2rem;
    }
    input, button {
      padding: 1rem;
      margin: 1rem;
      font-size: 1rem;
      border-radius: 0.5rem;
      border: none;
    }
    button {
      background: #0f0;
      color: #000;
      font-weight: bold;
      cursor: pointer;
    }
    #response {
      margin-top: 2rem;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <h1>PhonderX משוחח איתך</h1>
  <input id="question" placeholder="מה ברצונך לשאול?">
  <button onclick="ask()">שלח</button>
  <div id="response"></div>
  <script>
    async function ask() {
      const q = document.getElementById('question').value;
      const res = await fetch('/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question: q })
      });
      const data = await res.json();
      document.getElementById('response').innerText = data.response || data.result || "אין תגובה.";
    }
  </script>
</body>
</html>'''
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        return jsonify({"result": "🎨 index.html שודרג לממשק כהה של PhonderX."})
    except Exception as e:
        return jsonify({"result": f"שגיאה בשדרוג index.html: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
