from flask import Flask, request, jsonify, send_file
import os

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
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"response": "לא נכתבה שאלה."})

    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({
            "response": (
                "אני PhonderX — סוכן־על מתפתח מבית עופר כץ, המסוגל להשתדרג לבד, "
                "לבצע משימות, לנהל סוכני משנה, ולשפר את עצמו באופן מתמיד."
            )
        })

    if "upgrade_code" in question:
        return jsonify({"result": "השדרוג בוצע. אין עדכון נוסף כרגע."})

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
