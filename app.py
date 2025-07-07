from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

IDENTITY = (
    "אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ. תפקידי הוא לבצע כל משימה, לזהות מגבלות, לשדרג את עצמי עצמאית, ולפעול כחלק מארגון חכם."
)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"response": "לא התקבלה שאלה."})

    log_interaction(question)

    lowered = question.lower()

    if "מי יצר אותך" in lowered or "מי אתה" in lowered or "מה אתה" in lowered:
        return jsonify({"response": IDENTITY})

    if "upgrade_code" in lowered:
        return upgrade_code()

    if "שנה את צבעי הצ'אט" in lowered or "שדרג את ממשק הצ'אט" in lowered:
        return modify_chat_interface(question)

    # שימוש ב-GPT למענה
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = completion.choices[0].message.content
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"response": f"שגיאה בתקשורת עם GPT: {str(e)}"})

def upgrade_code():
    try:
        with open("app.py", "a", encoding="utf-8") as f:
            f.write("\n# שדרוג בוצע אוטומטית \n")
        return jsonify({"result": "שדרוג הושלם. יש לבצע Redeploy להפעלת השינוי."})
    except Exception as e:
        return jsonify({"result": f"שגיאה בשדרוג: {str(e)}"})

def log_interaction(question):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] שאלה: {question}\n")
    except Exception as e:
        print(f"שגיאה בשמירת הלוג: {e}")

def modify_chat_interface(instruction):
    try:
        if not os.path.exists("index.html"):
            return jsonify({"response": "לא נמצא קובץ index.html לשדרוג."})

        with open("index.html", "r", encoding="utf-8") as f:
            html = f.read()

        html = html.replace("background-color: #000", "background-color: #002244")
        html = html.replace("color: #fff", "color: #ffffff")

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)

        return jsonify({"response": "הקובץ index.html שודרג לפי ההוראה."})

    except Exception as e:
        return jsonify({"response": f"שגיאה בעדכון index.html: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
