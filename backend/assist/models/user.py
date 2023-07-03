from flaskext.auth.models.sa import get_user_class

# from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# import uuid


User = get_user_class(db.Model)
