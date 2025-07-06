from flask import Flask, request, jsonify, send_file
import os
import requests

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

    if "upgrade_code" in question or "שדרג את עצמך" in question:
        return auto_upgrade()

    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({"response": (
            "אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ. "
            "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם. "
            "אני מסוגל לעדכן את הקוד שלי, לבנות סוכני משנה, ולהשתפר כל הזמן."
        )})

    return jsonify({"response": f"שמעתי: {question}. אני עדיין לומד — תן לי רגע לחשוב על תשובה."})

@app.route("/auto_upgrade", methods=["POST"])
def auto_upgrade():
    try:
        url = "https://raw.githubusercontent.com/oferkatz/PhonderX/main/app.py"  # 👈 פה שמתי עבורך
        response = requests.get(url)
        if response.status_code == 200:
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(response.text)
            return jsonify({"result": "הקוד שודרג. יש לבצע Redeploy להפעלת השינוי."})
        else:
            return jsonify({"error": f"שגיאה בשליפת קוד ({response.status_code})"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
