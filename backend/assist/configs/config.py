"""Flask configuration variables."""
from os import getenv
import random
import string

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
# print(basedir)


class Config(object):
    """Set Flask configuration from .env file."""

    # General Config
    DEBUG = False
    TESTING = False
    SECRET_KEY = getenv("SECRET_KEY", None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(
            random.choice(
                string.ascii_letters
            ) for i in range(32)
        )
    FLASK_ENV = getenv("FLASK_ENV")

    # Database
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
