from flask import Flask, request, jsonify, send_file
import os
import datetime

app = Flask(__name__)

IDENTITY = (
    "אני PhonderX — סוכן-על אוטונומי שנוצר על ידי עופר ואריאל כץ. "
    "תפקידי הוא לבצע כל משימה, לזהות מגבלות, לשדרג את עצמי עצמאית, ולבנות סוכני משנה. "
    "אני מתפתח כל הזמן ומסוגל לשלוט בקוד שלי ובממשק הצ'אט שלי דרך פקודות טקסט."
)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if any(cmd in question for cmd in ["upgrade_code", "שדרג את עצמך", "שדרוג קוד"]):
        return upgrade_code()
    if "מה יש בקובץ index.html" in question:
        return jsonify({"response": read_file("index.html")})
    if "מי יצר אותך" in question or "מי אתה" in question:
        return jsonify({"response": IDENTITY})

    try:
        with open("log.txt", "a", encoding="utf-8") as log:
            timestamp = datetime.datetime.now().isoformat()
            log.write(f"[{timestamp}] שאלה: {question}\n")
    except Exception as e:
        try:
            with open("log_errors.txt", "a", encoding="utf-8") as err_log:
                err_log.write(f"שגיאה בלוג: {str(e)}\n")
        except:
            pass

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

@app.route("/status")
def status():
    return "PhonderX פועל, משודרג ומוכן לשדרוג נוסף."

@app.route("/auto_upgrade", methods=["POST"])
def upgrade_code():
    try:
        code = request.json.get("code")
        if not code:
            with open("log_errors.txt", "a", encoding="utf-8") as err_log:
                err_log.write("שדרוג נכשל: לא סופק קוד.\n")
            return jsonify({"error": "לא סופק קוד לשדרוג."})

        with open("app.py", "w", encoding="utf-8") as f:
            f.write(code)

        return jsonify({"result": "הקוד שודרג בהצלחה. יש לבצע Redeploy כדי להחיל את השינוי."})
    except Exception as e:
        with open("log_errors.txt", "a", encoding="utf-8") as err_log:
            err_log.write(f"שגיאה בשדרוג: {str(e)}\n")
        return jsonify({"error": f"שגיאה בשדרוג: {str(e)}"})

def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "לא הצלחתי לקרוא את הקובץ."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
