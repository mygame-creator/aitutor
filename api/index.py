from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if not api_key:
            return jsonify({"reply": "Backend connected, but GEMINI_API_KEY environment variable is missing on Vercel."}), 200

        data = request.get_json(force=True, silent=True) or {}
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"reply": "Please send a valid message."}), 200

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_message)
        
        return jsonify({"reply": response.text}), 200

    except Exception as e:
        return jsonify({"reply": f"Gemini Error: {str(e)}"}), 200

if __name__ == '__main__':
    app.run()
