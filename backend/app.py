"""Main Application API Routes"""

from flask import Flask, render_template, request, jsonify
from ai_engine.engine import Ai_Engine


app = Flask(__name__)
engine = Ai_Engine()

engine.main()


@app.route('/sign-up', methods=['POST'])
def sign_up():
    pass


@app.route('/login', methods=['POST'])
def login():
    pass


@app.route('/chat', methods=['POST'])
def chat():
    """Interact with Engine as a User"""
    user_input = request.json.get('user_input')

    response = engine.get_bot_response(user_input)

    response_data = {
        'response': response
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run()
