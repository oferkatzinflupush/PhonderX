from flask import Flask, request, jsonify, send_file
import os
import json
import datetime
import subprocess
import shutil
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

MEMORY_FILE = "memory.json"
ANSWERS_FILE = "answers.json"
AGENTS_FILE = "agents.json"
RULES_FILE = "system_rules.json"
MEMORY, ANSWERS, AGENTS, RULES = [], [], [], []

for file, store in [(MEMORY_FILE, MEMORY), (ANSWERS_FILE, ANSWERS), (AGENTS_FILE, AGENTS), (RULES_FILE, RULES)]:
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                store.extend(data)
        except Exception as e:
            print(f"שגיאה בטעינת {file}: {e}")

@app.route("/")
def home():
    return send_file("index.html") if os.path.exists("index.html") else "PhonderX is alive and online."

@app.route("/status")
def status():
    return "PhonderX פועל ומשודרג ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    timestamp = datetime.datetime.now().isoformat()
    log_event(question, timestamp)

    if "מי אתה" in question:
        response = "אני PhonderX — מערכת סוכנים אוטונומית שנבנתה ע״י עופר ואריאל כץ. אני יודע לשדרג את עצמי, לכתוב קוד, להריץ קבצים, לנהל סוכנים, ולהגן על עצמי."
    elif "מה שאלתי אותך קודם" in question:
        response = recall_last()
    elif "שדרג את ממשק הצ'אט" in question:
        return update_index_dark()
    elif "upgrade_code" in question:
        return safe_upgrade_code()
    elif "מצא בעיה בקוד שלך" in question:
        return diagnose_and_fix_code()
    elif "צור קובץ" in question and "עם התוכן" in question:
        return create_custom_file(question)
    elif "הרץ את הקובץ" in question:
        return execute_generated_code(question)
    elif "כתוב קוד" in question:
        return generate_code_with_gpt(question)
    elif "צור סוכן" in question:
        return register_agent(question)
    elif "בצע משימה" in question:
        return delegate_task_to_agent(question)
    elif "שחזר לגרסה הקודמת" in question:
        return restore_previous_backup()
    else:
        response = f"PhonderX קיבל את השאלה: {question}"

    record(question, response, timestamp)
    return jsonify({"response": response})

def log_event(question, timestamp):
    try:
        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"[{timestamp}] שאלה: {question}
")
    except Exception as e:
        print(f"שגיאה בלוג: {e}")

def record(q, a, t):
    MEMORY.append({"time": t, "q": q, "a": a})
    ANSWERS.append({"time": t, "question": q, "answer": a})
    for name, store in [(MEMORY_FILE, MEMORY), (ANSWERS_FILE, ANSWERS)]:
        try:
            with open(name, "w", encoding="utf-8") as f:
                json.dump(store, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"שגיאה בשמירת {name}: {e}")

def recall_last():
    if len(MEMORY) < 2:
        return "אני זוכר רק את השאלה האחרונה שלך."
    prev = MEMORY[-2]
    return f"השאלה הקודמת שלך הייתה: '{prev['q']}' ואני עניתי: '{prev['a']}'"

def register_agent(text):
    try:
        parts = text.split("צור סוכן")[-1].split("עם תפקיד")
        name = parts[0].strip()
        role = parts[1].strip() if len(parts) > 1 else "עוזר כללי"
        agent = {"name": name, "role": role, "tasks": []}
        AGENTS.append(agent)
        with open(AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(AGENTS, f, ensure_ascii=False, indent=2)
        return jsonify({"response": f"✅ הסוכן {name} נרשם עם תפקיד: {role}"})
    except Exception as e:
        return jsonify({"response": f"שגיאה ברישום סוכן: {str(e)}"})

def delegate_task_to_agent(text):
    try:
        task = text.replace("בצע משימה", "").strip()
        if not AGENTS:
            return jsonify({"response": "❗ אין סוכנים רשומים במערכת."})
        agent = AGENTS[0]
        agent['tasks'].append(task)
        with open(AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(AGENTS, f, ensure_ascii=False, indent=2)
        return jsonify({"response": f"📤 המשימה הועברה לסוכן {agent['name']}: {task}"})
    except Exception as e:
        return jsonify({"response": f"שגיאה בהעברת משימה: {str(e)}"})

def safe_upgrade_code():
    if not os.path.exists("app.py"):
        return jsonify({"response": "לא נמצא קובץ app.py לשדרוג."})
    if any("block_upgrade" in rule for rule in RULES):
        return jsonify({"response": "⛔️ השדרוג נחסם לפי חוקי המערכת."})
    backup_file = f"app_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy("app.py", backup_file)
    try:
        with open("app.py", "a", encoding="utf-8") as f:
            f.write("
# שדרוג בוצע: תוספת בדיקות הגנה")
        return jsonify({"response": f"✅ שדרוג בוצע. גיבוי נוצר: {backup_file}"})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשדרוג הקוד: {str(e)}"})

def restore_previous_backup():
    try:
        backups = [f for f in os.listdir() if f.startswith("app_backup") and f.endswith(".py")]
        if not backups:
            return jsonify({"response": "לא נמצאו גיבויים לשחזור."})
        latest = sorted(backups)[-1]
        shutil.copy(latest, "app.py")
        return jsonify({"response": f"🔄 שוחזרה גרסה מ־{latest}"})
    except Exception as e:
        return jsonify({"response": f"שגיאה בשחזור: {str(e)}"})

def generate_code_with_gpt(prompt):
    try:
        instruction = f"כתוב קוד Python עבור: {prompt}"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": instruction}]
        )
        code = completion.choices[0].message['content']
        filename = "generated_code.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        return jsonify({"response": f"✅ הקוד נוצר ונשמר ל־{filename} בהצלחה."})
    except Exception as e:
        return jsonify({"response": f"שגיאה ביצירת קוד GPT: {str(e)}"})

def create_custom_file(instruction):
    try:
        parts = instruction.split("צור קובץ")[-1].split("עם התוכן")
        if len(parts) != 2:
            return jsonify({"response": "לא הצלחתי לפענח את שם הקובץ או התוכן."})
        filename = parts[0].strip().replace(""", "").replace("'", "")
        content = parts[1].strip()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return jsonify({"response": f"✅ הקובץ {filename} נוצר בהצלחה."})
    except Exception as e:
        return jsonify({"response": f"שגיאה ביצירת קובץ: {str(e)}"})

def execute_generated_code(instruction):
    try:
        words = instruction.split()
        for word in words:
            if word.endswith(".py") and os.path.exists(word):
                output = subprocess.check_output(["python3", word], stderr=subprocess.STDOUT)
                return jsonify({"response": f"✅ הקובץ {word} רץ בהצלחה. פלט:
{output.decode()}"} )
        return jsonify({"response": "❗ לא נמצא קובץ להרצה."})
    except subprocess.CalledProcessError as e:
        return jsonify({"response": f"שגיאה בהרצת הקובץ:
{e.output.decode()}"} )
    except Exception as e:
        return jsonify({"response": f"שגיאה כללית: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
