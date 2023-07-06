# assist/server/__init__.py
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'assist.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
jwt = JWTManager()
db = SQLAlchemy()
mail = Mail(app)

from assist.server.auth.views import auth_blueprint

app.register_blueprint(auth_blueprint)
