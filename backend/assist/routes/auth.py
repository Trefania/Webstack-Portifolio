from app import app
from assist.configs.alchemyinit import db
from flask import request, jsonify
from models.user import User
from flaskext.auth.auth import login, logout, login_required, get_current_user_data


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome():
    """ Welcome Message """
    return 'Welcome to Assist AI'


@app.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """ add new user """
    email = request.form['email']
    password = request.form['password']

    existing_user = User.query.filter_by(username=email).first()
    if existing_user:
        return 'Email already exists', 409

    new_user = User(username=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    login(new_user)

    return 'User registered successfully', 200


@app.route('/login', methods=['POST'], strict_slashes=False)
def signin():
    """ User SignIn """
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(username=email).first()
    if user.authenticate(password):
        return 'Login successful', 200
    else:
        return 'Invalid credentials'


@app.route('/logout', methods=['POST'], strict_slashes=False)
def optout():
    user = logout()
    return f'Logged {user} out successfully'


@app.route('/protected', strict_slashes=False)
@login_required()
def home():
    user = get_current_user_data()
    return jsonify(user)
