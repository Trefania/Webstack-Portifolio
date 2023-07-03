import os
from flask import Flask
from flaskext.auth.auth import Auth
from assist.configs.config import Config
from assist.configs.alchemyinit import db, init_app
# from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    db.app = app
    init_app(app)
    auth = Auth(app)

    return app
