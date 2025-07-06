from flask import Flask, request, jsonify, send_from_directory
import os
import openai
import json

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

MEMORY_FILE = "memory.json"

# תיעוד מגבלות
def log_limitation(question, reason):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "שאלה": question,
            "למה הוא נכשל": reason
        }, ensure_ascii=False) + "\n")

# שליפה של כל הזיכרון
def get_limitations():
    if not os.path.exists(MEMORY_FILE):
        return "אין לי תיעוד של בעיות כרגע."
    
    with open(MEMORY_FILE, encoding="utf-8") as f:
        lines = f.readlines()
        return "\n".join(lines) if lines else "אין לי תיעוד של בעיות כרגע."

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question", "")

        # אם המשתמש שואל על המגבלות של PhonderX
        if "מה לא הצלחת" in question or "מה לא הצליח" in question or "מה אתה לא יודע" in question:
            return jsonify({"response": get_limitations()})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "אתה PhonderX — סוכן־על שלומד, זוכר, מתעד ומפעיל סוכנים. "
                        "אם אינך מצליח לבצע משימה, אתה מתעד אותה לזיכרון פנימי. "
                        "אם נשאלת שאלה על מגבלותיך — קרא מתוך הזיכרון ושקף את זה."
                    )
                },
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"שגיאה: {str(e)}"
        log_limitation(question, str(e))

    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
