from flask import Flask, request, jsonify, send_from_directory
import os
import openai
import json

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

MEMORY_FILE = "memory.json"
UPGRADE_FILE = "pending_upgrades.json"

# תיעוד מגבלות
def log_limitation(question, reason):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "שאלה": question,
            "למה הוא נכשל": reason
        }, ensure_ascii=False) + "\n")

# הצגת מגבלות קיימות
def get_limitations():
    if not os.path.exists(MEMORY_FILE):
        return "אין לי תיעוד של מגבלות כרגע."
    with open(MEMORY_FILE, encoding="utf-8") as f:
        lines = f.readlines()
        return "\n".join(lines) if lines else "אין לי תיעוד של מגבלות כרגע."

# שדרוג עצמי בפועל
def upgrade_code(code_str):
    try:
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(code_str)
        return "קובץ app.py שודרג בהצלחה 🎉"
    except Exception as e:
        return f"שגיאה בשדרוג עצמי: {str(e)}"

# שמירת שדרוג לקובץ נפרד (לא חובה)
def save_upgrade(code, title="שדרוג ללא שם"):
    upgrade = {"שם": title, "קוד": code}
    upgrades = []
    if os.path.exists(UPGRADE_FILE):
        with open(UPGRADE_FILE, encoding="utf-8") as f:
            upgrades = json.load(f)
    upgrades.append(upgrade)
    with open(UPGRADE_FILE, "w", encoding="utf-8") as f:
        json.dump(upgrades, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question", "")

        if any(p in question for p in [
            "מה לא הצלחת", "מה לא הצליח", "מה אתה לא יודע",
            "מה הדברים שאתה לא יודע לעשות", "מה אתה עוד לא יודע",
            "מה לא עבד", "מה המשימות שלא הצלחת", "מה קרה כשלא הצלחת"
        ]):
            return jsonify({"response": get_limitations()})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "אתה PhonderX — סוכן־על מתפתח. "
                        "אם אתה נתקל בבעיה או דרישה לשדרוג, "
                        "צור גרסת קוד חדשה ל־app.py, והשתמש ב־upgrade_code כדי להחיל אותה בפועל."
                    )
                },
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content

        # הפעלה אוטומטית של שדרוג אם הקוד מופיע
        if "upgrade_code(" in answer and "```" in answer:
            code_block = answer.split("```")[1].split("```")[0]
            result = upgrade_code(code_block)
            answer += f"\n\n[שדרוג בוצע]: {result}"

        return jsonify({"response": answer})

    except Exception as e:
        log_limitation(question, str(e))
        return jsonify({"response": f"שגיאה: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
