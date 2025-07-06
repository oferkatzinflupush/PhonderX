from flask import Flask, request, jsonify, send_file
import os
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/status")
def status():
    return "PhonderX פעול ומשודרג ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").lower()

    if any(kw in question for kw in ["upgrade_code", "תשדרג את עצמך", "שדרג את עצמך", "התעל שדרוג"]):
        return auto_upgrade()

    if any(kw in question for kw in ["מי אתה", "מה אתה"]):
        return jsonify({"response": (
            "אני PhonderX — סוכן‏-על משודרג, יצירה של עופר ואריאל כץ. "
            "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמית, ולפעל כחלק מארגון חכם."
        )})

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

@app.route("/auto_upgrade", methods=["POST"])
def auto_upgrade():
    try:
        url = "https://raw.githubusercontent.com/oferkatzinflux/phonderx/main/app.py"
        response = requests.get(url)
        if response.status_code == 200:
            new_code = response.text
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(new_code)
            return jsonify({"result": "קוד המועדן הצלחה. אנא עשה Redeploy כדי להפעיל."})
        else:
            return jsonify({"error": f"שגיאה בשליפה מהכתובת. Status: {response.status_code}"})
    except Exception as e:
        return jsonify({"error": f"שגיאה: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
