from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PhonderX פועל ומשודרג ✅"

@app.route("/status")
def status():
    return "PhonderX תקין ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    if "שדרג את עצמך" in question:
        return upgrade_code()

    log_interaction(question)

    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def upgrade_code():
    try:
        new_code = """from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PhonderX פועל ומשודרג ✅"

@app.route("/status")
def status():
    return "PhonderX פועל באופן מלא ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    log_interaction(question)
    return jsonify({"response": f"PhonderX קיבל את השאלה: {question}"})

def log_interaction(text):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(text + "\\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
"""
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(new_code)
        return jsonify({"result": "הקוד שודרג בהצלחה. נדרש redeploy להפעלה מחדש."})
    except Exception as e:
        return jsonify({"error": str(e)})

def log_interaction(text):
    try:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except:
        pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
