from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

IDENTITY = (
    "אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ. "
    "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם. "
    "אני מסוגל לעדכן את הקוד שלי, לבנות סוכני משנה, ולהשתפר כל הזמן."
)

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

    if "מי אתה" in question or "מה אתה" in question:
        log(question)
        return jsonify({"response": IDENTITY})

    if "שדרג את עצמך" in question:
        return upgrade_code()

    log(question)
    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def upgrade_code():
    try:
        upgraded = """from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

IDENTITY = ("""
אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ.
תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם.
אני מסוגל לעדכן את הקוד שלי, לבנות סוכני משנה, ולהשתפר כל הזמן.
""")

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

    if "מי אתה" in question or "מה אתה" in question:
        log(question)
        return jsonify({"response": IDENTITY})

    log(question)
    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def log(text):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(text + "\\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
"""
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(upgraded)
        return jsonify({"result": "הקוד שודרג בהצלחה! נדרש redeploy."})
    except Exception as e:
        return jsonify({"error": str(e)})

def log(text):
    try:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except:
        pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
