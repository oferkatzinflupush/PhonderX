from flask import Flask, request, jsonify, send_from_directory
import os
import openai
import json

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# פונקציית תיעוד שדרוג עצמי
def log_limitation(question, reason):
    with open("memory.json", "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "שאלה": question,
            "למה הוא נכשל": reason
        }, ensure_ascii=False) + "\n")

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question", "")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "אתה PhonderX — סוכן־על שנוצר על ידי עופר ואריאל כץ. "
                        "תפקידך לזהות בעיות, להפעיל סוכנים תחתיך, להשתדרג ולהתמודד עם כל אתגר. "
                        "אם אינך יודע משהו — תעד את זה לתוך 'memory.json' כדי לעזור לשדרוג עתידי."
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
