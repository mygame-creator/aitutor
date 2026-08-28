from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Fetch API key from Vercel Environment Variables
api_key = os.environ.get("AQ.Ab8RN6KvDDQvWB1C0L18KYma8FzFsbuFiQ-xnBtcXbqzc-AB7w")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get('message', '')

        if not api_key:
            return jsonify({"reply": "Error: GEMINI_API_KEY is not configured in Vercel settings."}), 500

        if not user_message:
            return jsonify({"reply": "Please enter a message."}), 400

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500

# Vercel needs the WSGI app instance exposed as 'app'
if __name__ == '__main__':
    app.run()
