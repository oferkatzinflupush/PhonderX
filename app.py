from flask import Flask, request, jsonify, send_file
import os
import json
from datetime import datetime

app = Flask(__name__)

IDENTITY = (
    "אני PhonderX — סוכן־על אוטונומי מתפתח, יצירה של עופר ואריאל כץ. "
    "המטרה שלי היא לבצע כל משימה, להשתפר כל הזמן, לנהל סוכני־משנה, "
    "לשדרג את עצמי, לשנות עיצוב, לזכור שיחות, ולעולם לא לאבד את הקשר איתך."
)

AGENTS_FILE = "agents.json"
if not os.path.exists(AGENTS_FILE):
    with open(AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

@app.route("/")
def home():
    return send_file("index.html") if os.path.exists("index.html") else "PhonderX פעיל ✅"

@app.route("/status")
def status():
    return "PhonderX פועל ומוכן 🧠"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    log(question)

    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({"response": IDENTITY})

    if "upgrade_code" in question or "שדרג את הקוד שלך" in question:
        return upgrade_self()

    if "שנה את צבעי הצ'אט" in question or "שדרג את הממשק" in question:
        return change_chat_colors()

    if "צור סוכן" in question:
        return create_agent(question)

    if "בצע משימה" in question:
        return assign_task_to_agent(question)

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})


def log(text):
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] שאלה: {text}\n")
    except Exception as e:
        print("שגיאה בלוג:", e)

def upgrade_self():
    try:
        with open("app.py", "a", encoding="utf-8") as f:
            f.write("\n# ✅ שדרוג עצמי נוסף בוצע.")
        return jsonify({"response": "✅ שדרוג פנימי הושלם. הקובץ app.py עודכן."})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשדרוג: {str(e)}"})

def change_chat_colors():
    try:
        html = '''<!DOCTYPE html>
<html lang="he">
<head>
  <meta charset="UTF-8">
  <title>PhonderX</title>
  <style>
    body {
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: monospace;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem;
    }
    input, button {
      padding: 0.75rem;
      font-size: 1rem;
      margin: 1rem;
      border-radius: 0.5rem;
      border: none;
    }
    button {
      background-color: #58a6ff;
      color: white;
      font-weight: bold;
      cursor: pointer;
    }
    #response {
      margin-top: 2rem;
      white-space: pre-wrap;
      text-align: left;
      max-width: 600px;
    }
  </style>
</head>
<body>
  <h1>PhonderX</h1>
  <input id="question" placeholder="מה ברצונך לשאול?">
  <button onclick="send()">שלח</button>
  <div id="response"></div>
  <script>
    async function send() {
      const q = document.getElementById("question").value;
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
      });
      const data = await res.json();
      document.getElementById("response").innerText = data.response || data.result || "אין תגובה.";
    }
  </script>
</body>
</html>'''
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        return jsonify({"response": "🎨 צבעי הממשק שודרגו בהצלחה."})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשינוי צבעים: {str(e)}"})

def create_agent(text):
    try:
        parts = text.split("צור סוכן")[-1].strip().split("עם תפקיד")
        name = parts[0].strip()
        role = parts[1].strip() if len(parts) > 1 else "לא צוין"
        with open(AGENTS_FILE, "r", encoding="utf-8") as f:
            agents = json.load(f)
        agents.append({"name": name, "role": role, "tasks": []})
        with open(AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(agents, f, ensure_ascii=False, indent=2)
        return jsonify({"response": f"🤖 סוכן חדש בשם {name} עם תפקיד: {role} נוצר ונשמר."})
    except Exception as e:
        return jsonify({"response": f"שגיאה ביצירת סוכן: {str(e)}"})

def assign_task_to_agent(text):
    try:
        task = text.split("בצע משימה")[-1].strip()
        with open(AGENTS_FILE, "r", encoding="utf-8") as f:
            agents = json.load(f)
        if not agents:
            return jsonify({"response": "⚠️ אין סוכנים רשומים במערכת."})
        agents[0]["tasks"].append(task)
        with open(AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(agents, f, ensure_ascii=False, indent=2)
        return jsonify({"response": f"📤 המשימה הועברה לסוכן {agents[0]['name']}: {task}"})
    except Exception as e:
        return jsonify({"response": f"שגיאה בהקצאת משימה: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
