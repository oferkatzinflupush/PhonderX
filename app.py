<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PhonderX Chat</title>
  <style>
    body {
      background-color: #000;
      color: #fff;
      font-family: sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    #chat-container {
      background: #1a1a1a;
      padding: 2rem;
      border-radius: 1rem;
      box-shadow: 0 0 10px #00ff88;
      width: 90%;
      max-width: 500px;
    }
    h2 {
      text-align: center;
      margin-bottom: 1rem;
    }
    input[type="text"] {
      width: 100%;
      padding: 0.5rem;
      margin-bottom: 1rem;
      border-radius: 0.5rem;
      border: none;
      outline: none;
      font-size: 1rem;
    }
    button {
      width: 100%;
      padding: 0.5rem;
      background-color: #00ff88;
      color: #000;
      font-weight: bold;
      border: none;
      border-radius: 0.5rem;
      cursor: pointer;
    }
    #response {
      margin-top: 1rem;
      white-space: pre-wrap;
      font-family: monospace;
    }
  </style>
</head>
<body>
  <div id="chat-container">
    <h2>PhonderX משוחח איתך</h2>
    <input type="text" id="question" placeholder="מה ברצונך לשאול?">
    <button onclick="sendQuestion()">שלח</button>
    <div id="response"></div>
  </div>

  <script>
    async function sendQuestion() {
      const question = document.getElementById('question').value;
      const responseDiv = document.getElementById('response');
      responseDiv.innerText = "טוען תגובה...";
      try {
        const res = await fetch('/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ question })
        });
        const data = await res.json();
        responseDiv.innerText = data.response || data.result || "לא התקבלה תגובה.";
      } catch (e) {
        responseDiv.innerText = "שגיאה בשליחה: " + e.message;
      }
    }
  </script>
</body>
</html>
