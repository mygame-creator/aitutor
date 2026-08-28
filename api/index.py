from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("AQ.Ab8RN6KvDDQvWB1C0L18KYma8FzFsbuFiQ-xnBtcXbqzc-AB7w")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get('message', '')

        if not api_key:
            return jsonify({"reply": "Error: GEMINI_API_KEY is not set in Vercel environment variables."}), 500

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Server Error: {str(e)}"}), 500
