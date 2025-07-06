from flask import Flask, request, jsonify, send_file
import os
import requests

app = Flask(__name__)

# --- Home route that serves index.html if available ---
@app.route("/")
def home():
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(index_path):
        return send_file(index_path)
    return "PhonderX is alive and online."

# --- Status check ---
@app.route("/status")
def status():
    return "PhonderX פעל ומשודרג ✅"

# --- Main chat interaction ---
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if "upgrade_code" in question:
        return upgrade_code()
    if "מי אתה" in question or "מה אתה" in question:
        return jsonify({"response": (
            "אני PhonderX — סוכן‏-על מתפתח, יצירה של עופר ואריאל כץ. "
            "תפקידי הוא לבצע כל משימה, לזהות מגבלות, להשתדרג עצמאית, ולפעול כחלק מארגון חכם."
        )})

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

# --- Auto upgrade via external URL ---
@app.route("/auto_upgrade", methods=["POST"])
def auto_upgrade():
    try:
        url = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/app.py"  # Replace!
        response = requests.get(url)
        if response.status_code == 200:
            new_code = response.text
            with open("app.py", "w", encoding="utf-8") as f:
                f.write(new_code)
            return jsonify({"result": "הקוד שודרג אוטומטית. נדרש Redeploy להפעלת השינוי."})
        else:
            return jsonify({"error": f"שליפת קוד נכשלה ({response.status_code})"})
    except Exception as e:
        return jsonify({"error": str(e)})

# --- Manual upgrade command (used via /ask) ---
def upgrade_code():
    return jsonify({"result": "השדרוג בוצע. אין עדכון נוסף כרגע."})

# --- Run the app ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
