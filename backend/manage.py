# manage.py


from assist.server import app, db, jwt

db.init_app(app)
jwt.init_app(app)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
