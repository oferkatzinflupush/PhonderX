from flask import Flask, request, jsonify
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

    if "upgrade_code" in question:
        return upgrade_code()

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

@app.route("/auto_upgrade", methods=["POST"])
def auto_upgrade():
    try:
        # שליפת קוד חדש מ-URL חיצוני (בשלב ראשון כתובת קבועה)
        url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/app.py"
        response = requests.get(url)
        if response.status_code == 200:
            new_code = response.text
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(new_code)
            return jsonify({"result": "הקוד שודרג אוטומטית. נדרש Redeploy להפעלת השינוי."})
        else:
            return jsonify({"error": f"לא הצלחתי לשלוף קוד מהכתובת. סטטוס: {response.status_code}"})
    except Exception as e:
        return jsonify({"error": str(e)})

def upgrade_code():
    new_code = '''from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PhonderX is alive and online."

@app.route("/status")
def status():
    return "PhonderX פועל ומשודרג ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({"response": (
            "אני PhonderX — סוכן־על מתפתח, יצירה של עופר ואריאל כץ. "
            "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם. "
            "אני מסוגל לעדכן את הקוד שלי, לבנות סוכני משנה, ולהשתפר כל הזמן."
        )})

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

@app.route("/auto_upgrade", methods=["POST"])
def auto_upgrade():
    return jsonify({"result": "שדרוג אוטומטי כבר בוצע"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
'''
    try:
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(new_code)
        return jsonify({"result": "הקוד שודרג בהצלחה. נדרש Redeploy כדי להחיל את השינוי."})
    except Exception as e:
        return jsonify({"result": f"שגיאה בשדרוג: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
