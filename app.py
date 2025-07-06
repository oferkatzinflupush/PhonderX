from flask import Flask, request, jsonify, send_file
import os
import openai

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

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

    if "שדרג את הממשק" in question or "תשנה את הצ'אט" in question or "כתוב ממשק חדש" in question:
        return generate_and_save_ui(question)

    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({"response": (
            "אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ. "
            "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם. "
            "אני מסוגל לעדכן את הקוד שלי, לבנות סוכני משנה, ולהשתפר כל הזמן."
        )})

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def generate_and_save_ui(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "כתוב קובץ HTML מלא לפי הבקשה, בלי הסברים. התחל ב-<!DOCTYPE html>."},
                {"role": "user", "content": prompt}
            ]
        )
        html_code = response.choices[0].message.content
        if "<!DOCTYPE html>" in html_code:
            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html_code)
            return jsonify({"result": "✅ הקובץ index.html שודרג לפי ההוראה."})
        else:
            return jsonify({"error": "לא נוצר קוד HTML תקני."})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
