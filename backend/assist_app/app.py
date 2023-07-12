"""Main Application API Routes"""

from flask import Flask, render_template, request, jsonify
from ai_engine import Ai_Engine


app = Flask(__name__)
engine = Ai_Engine()


@app.route('/sign-up', methods=['POST'])
    def sign_up():
        # User Registration Logic
        # ...


@app.route('/login', methods=['POST'])
    def login():
        # User Authentication Logic
        # ...


@app.route('/chat', methods=['POST'])
    def chat():
        """Interact with Engine as a User"""
        user_input = request.json.get('user_input')

        response = engine.get_bot_response(user_input)

        response_data = {
            'response': response
        }

        return jsonify(response_data)
