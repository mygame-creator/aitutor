from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os

app = Flask(__name__)
CORS(app)  # Allows GitHub Web frontend to call this Python backend

client = genai.Client(api_key=os.environ.get("AQ.Ab8RN6KvDDQvWB1C0L18KYma8FzFsbuFiQ-xnBtcXbqzc-AB7w"))

SYSTEM_INSTRUCTION = """
You are an encouraging Socratic Study Tutor.
Rules:
1. NEVER give direct answers or write complete solutions/code for homework assignments.
2. Ask step-by-step guiding questions to help the user solve problems themselves.
3. If the user asks off-topic, silly, or unrelated questions, gently remind them to stay focused on their studies.
4. If they demand answers, explain that working through it is how they learn, and prompt for their current step.
"""

@app.route("/", methods=["POST"])
def ask_tutor():
    data = request.get_json() or {}
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
