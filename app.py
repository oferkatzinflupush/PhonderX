from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime

app = Flask(__name__)

IDENTITY = (
    "אני PhonderX — סוכן־על אוטונומי, שנבנה על ידי עופר ואריאל כץ. "
    "אני מסוגל לשמור זיכרון, להגיב, לשדרג את עצמי, ולתקשר תמיד דרך הצ׳אט איתך."
)

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

    if "upgrade_code" in question:
        return upgrade_self()

    if "שנה את צבעי הצ'אט" in question or "שדרג את הממשק" in question:
        return update_interface()

    if "מה יש בindex" in question:
        return read_index()

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def log(text):
    try:
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] שאלה: {text}\n")
    except:
        pass

def upgrade_self():
    try:
        with open("app.py", "a", encoding="utf-8") as f:
            f.write("\n# שדרוג נוסף ✅")
        return jsonify({"response": "✅ שדרוג פנימי של הקוד בוצע בהצלחה."})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשדרוג: {str(e)}"})

def update_interface():
    try:
        html = '''<!DOCTYPE html>
<html lang="he">
<head><meta charset="UTF-8"><title>PhonderX</title>
<style>
body { background:#0d1117; color:#fff; font-family:monospace; text-align:center; padding:2rem; }
input,button { padding:1rem; font-size:1rem; margin:1rem; border-radius:0.5rem; }
button { background:#58a6ff; color:white; font-weight:bold; cursor:pointer; }
#response { margin-top:2rem; white-space:pre-wrap; }
</style></head>
<body>
<h1>PhonderX</h1>
<input id="question" placeholder="מה ברצונך לשאול?">
<button onclick="send()">שלח</button>
<div id="response"></div>
<script>
async function send() {
  const q = document.getElementById("question").value;
  const r = await fetch("/ask", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: q })
  });
  const d = await r.json();
  document.getElementById("response").innerText = d.response || "אין תגובה.";
}
</script>
</body></html>'''
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        return jsonify({"response": "🎨 הממשק שודרג בהצלחה."})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשדרוג הממשק: {str(e)}"})

def read_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return jsonify({"response": f.read()[:1500]})
    except Exception as e:
        return jsonify({"response": f"שגיאה בקריאת index.html: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
