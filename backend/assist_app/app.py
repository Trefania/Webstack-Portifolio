"""Main Application API Routes"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from ai_engine import Ai_Engine
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from pymongo import MongoClient

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_mysql_database'


engine = Ai_Engine()
mysql = MySQL(app)


# MongoDB Configuration
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['your_mongo_db']

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = sha256_crypt.encrypt(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO users (email, name, password) VALUES (%s, %s, %s)', (email, name, password))
        mysql.connection.commit()

        # Create new instance of MongoDB chat storage based on user_email
        chat_collection = db[email]

        session['email'] = email
        return redirect(url_for('profile'))

    return render_template('sign_up.html')


@app.route('/login', methods=['POST'])
def login():
   if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cur.fetchone()

        if user and sha256_crypt.verify(password, user['password']):
            session['email'] = email
            return redirect(url_for('profile'))

        return render_template('login.html', error='Invalid credentials')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'email' in session:
        # Check if the MongoDB chat collection exists for the user_email
        email = session['email']
        chat_collection = db[email]

        # Retrieve the chat history from the MongoDB collection (if needed)
        # chat_data = chat_collection.find({})

        return render_template('profile.html', email=session['email'])
    else:
        return redirect(url_for('login'))


@app.route('/profile/chats')
def view_chats():
    if 'email' in session:
        email = session['email']
        chat_collection = db[email]

        # Retrieve the last 10 chat titles from MongoDB
        chat_titles = chat_collection.find().sort('_id', -1).limit(10)

        return render_template('chat_titles.html', chat_titles=chat_titles)
    else:
        return redirect(url_for('login'))


@app.route('/profile/chats/new', methods=['GET', 'POST'])
def new_chat():
    if 'email' in session:
        if request.method == 'POST':
            # Create a new instance of MongoDB chat storage based on user_id (or email)
            email = session['email']
            chat_collection = db[email]

            # Generate a new chat_id and chat_title
            chat_id = str(datetime.now().timestamp()).replace('.', '')
            chat_title = f'Chat {chat_id}'

            # Store the new chat_id and chat_title in MongoDB
            chat_collection.insert_one({
                'chat_id': chat_id,
                'chat_title': chat_title,
                'messages': []  # To store user prompts and AI responses
            })

            return redirect(url_for('view_chat', chat_id=chat_id))

        return render_template('new_chat.html')
    else:
        return redirect(url_for('login'))
    

@app.route('/profile/chats/<string:chat_id>', methods=['GET', 'POST'])
def view_chat(chat_id):
    if 'email' in session:
        email = session['email']
        chat_collection = db[email]
        chat = chat_collection.find_one({'chat_id': chat_id})

        if not chat:
            return redirect(url_for('view_chats'))

        if request.method == 'POST':
            user_input = request.form['user_input']
            response = engine.get_bot_response(user_input)

            # Append the user prompt and AI response to the chat messages
            chat_collection.update_one({'chat_id': chat_id},
                                       {'$push': {'messages': {'user': user_input, 'response': response}}})

        return render_template('chat.html', chat=chat)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()