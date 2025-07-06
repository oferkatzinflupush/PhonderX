from flask import Flask, request, jsonify, send_from_directory
import os
import openai

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "אתה PhonderX, סוכן־על ארגוני שמשרת את עופר כץ. אתה עונה בעברית ונותן ייעוץ חכם ואנושי."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"שגיאה מהשרת: {str(e)}"

    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
