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
    if "index.html" in question or "שדרג את ממשק הצ'אט" in question:
        return handle_index_update(question)

    if "מי אתה" in question:
        return jsonify({"response": (
            "אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ. "
            "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם. "
            "אני מסוגל לעדכן את הקוד שלי, לבנות סוכני משנה, ולהשתפר כל הזמן."
        )})

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def upgrade_code():
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            current_code = f.read()
        return jsonify({"result": "השדרוג בוצע. אין עדכון נוסף כרגע."})
    except Exception as e:
        return jsonify({"result": f"שגיאה בשדרוג: {str(e)}"})

def handle_index_update(instruction):
    try:
        if "צבע שחור" in instruction and "טקסט ירוק" in instruction:
            html = generate_html("#000", "#00ff88")
        elif "צבע אפור" in instruction:
            html = generate_html("#333", "#ffffff")
        else:
            html = generate_html("#000", "#00ff88")

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        return jsonify({"result": "הקובץ index.html שודרג לפי ההוראה."})
    except Exception as e:
        return jsonify({"result": f"שגיאה בשדרוג הממשק: {str(e)}"})

def generate_html(bg_color, text_color):
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>PhonderX Chat</title>
  <style>
    body {{
      background-color: {bg_color};
      color: {text_color};
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }}
    #chat-container {{
      background: #1a1a1a;
      padding: 2rem;
      border-radius: 1rem;
      box-shadow: 0 0 10px {text_color};
      width: 90%;
      max-width: 500px;
    }}
    h2 {{ text-align: center; margin-bottom: 1rem; }}
    input[type=\"text\"] {{
      width: 100%;
      padding: 0.5rem;
      margin-bottom: 1rem;
      border-radius: 0.5rem;
      border: none;
      outline: none;
      font-size: 1rem;
    }}
    button {{
      width: 100%;
      padding: 0.5rem;
      background-color: {text_color};
      color: {bg_color};
      font-weight: bold;
      border: none;
      border-radius: 0.5rem;
      cursor: pointer;
    }}
    #response {{
      margin-top: 1rem;
      white-space: pre-wrap;
      font-family: monospace;
    }}
  </style>
</head>
<body>
  <div id=\"chat-container\">
    <h2>PhonderX משוחח איתך</h2>
    <input type=\"text\" id=\"question\" placeholder=\"מה ברצונך לשאול?\">
    <button onclick=\"sendQuestion()\">שלח</button>
    <div id=\"response\"></div>
  </div>

  <script>
    async function sendQuestion() {{
      const question = document.getElementById('question').value;
      const responseDiv = document.getElementById('response');
      responseDiv.innerText = \"טוען תגובה...\";
      try {{
        const res = await fetch('/ask', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ question }})
        }});
        const data = await res.json();
        responseDiv.innerText = data.response || data.result || \"לא התקבלה תגובה.\";
      }} catch (e) {{
        responseDiv.innerText = \"שגיאה בשליחה: \" + e.message;
      }}
    }}
  </script>
</body>
</html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
