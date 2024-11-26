import flask

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from ChatBot import ChatBot

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Initialize ChatBot instance
bot = ChatBot()

@app.route('/answer', methods=['POST'])
def get_answer():
    """Endpoint to receive a question and return an answer."""
    data = request.get_json()

    # Ensure the question is provided in the request
    if not data or 'question' not in data:
        return jsonify({"error": "Question not provided"}), 400

    question = data['question']
    
    # Get the answer from ChatBot
    try:
        answer = bot.answer(question)
        return jsonify({"question": question, "answer": answer}), 200
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)