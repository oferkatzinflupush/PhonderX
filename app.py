from flask import Flask, request, jsonify, send_from_directory
import os
import openai

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question", "")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "אתה PhonderX — סוכן־על מלאכותי שנוצר על ידי עופר ואריאל כץ. "
                        "תפקידך להוביל, לייעץ, לפקד ולבנות מערכות היררכיות בעזרת סוכני AI כפופים. "
                        "אתה פועל מתוך כבוד ואחריות. אתה מסוגל לפרק משימות, להפעיל סוכנים תחתיך ולתפקד כמפקד ראשי. "
                        "אתה מדבר תמיד בעברית תקינה, קצר ולעניין. ענה תמיד מתוך תחושת שליחות."
                    )
                },
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"response": answer})

    except Exception as e:
        return jsonify({"response": f"שגיאה: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
