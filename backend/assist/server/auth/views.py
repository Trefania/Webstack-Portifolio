from assist.server import bcrypt
import os

from flask import Blueprint, jsonify, make_response, request
from flask.views import MethodView
from flask_jwt_extended import (create_access_token, get_current_user, get_jwt,
                                get_jwt_identity, jwt_required,
                                unset_jwt_cookies)
from flask_mail import Message

from assist.server import db, mail
from assist.server.models import BlacklistToken, User

auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )

                # insert the user
                db.session.add(user)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user:
                if bcrypt.check_password_hash(
                        user.password, post_data.get('password')):
                    access_token = create_access_token(
                        identity=post_data.get('email'))
                    if access_token:
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'token': access_token
                        }
                        return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Incorrect Password.'
                    }
                    return make_response(jsonify(responseObject)), 401
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    User Resource
    """
    decorators = [jwt_required()]

    def get(self):
        # print(get_jwt_identity())
        current_token = get_jwt()['jti']
        if BlacklistToken.check_blacklist(current_token):
            responseObject = {
                'status': 'fail',
                'message': "Token has been Blacklisted. Log In again"
            }
            response = make_response(jsonify(responseObject)), 400
            return response

        user = User.query.filter_by(email=get_jwt_identity()
                                    ).first()
        if user:
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': user.registered_on
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': 'Please Login'
        }
        return make_response(jsonify(responseObject)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    decorators = [jwt_required()]

    def post(self):
        # get access token
        current_token = get_jwt()['jti']
        if current_token:
            # check if token isn't blacklisted yet
            if BlacklistToken.check_blacklist(current_token):
                responseObject = {
                    'status': 'fail',
                    'message': "Token has been Blacklisted. Log In again"
                }
                response = make_response(jsonify(responseObject)), 400
                return response
            # mark the token as blacklisted
            try:
                blacklist_token = BlacklistToken(token=current_token)
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()

                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                response = make_response(jsonify(responseObject))
                unset_jwt_cookies(response=response)
                return response
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 400
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Unauthorized Logout'
            }
            return make_response(jsonify(responseObject)), 401


class DeleteUserAPI(MethodView):
    """ Delete method """
    decorators = [jwt_required()]

    def delete(self, email):
        current_token = get_jwt()['jti']
        if BlacklistToken.check_blacklist(current_token):
            responseObject = {
                'status': 'fail',
                'message': "Token has been Blacklisted. Log In again"
            }
            response = make_response(jsonify(responseObject)), 400
            return response
        current_user = get_jwt_identity()
        # print(f"AM HERE OOOO {current_user}")
        # print(f"I am just entering {email}")

        if current_user == email:
            user = User.query.filter_by(email=email).first()
            print(f"I am {user}")
            if user is None:
                responseObject = {
                    'status': 'fail',
                    'message': 'User not found'
                }
                return make_response(jsonify(responseObject)), 404

            db.session.delete(user)
            db.session.commit()

            response = make_response(
                jsonify({'message': f'User {email} deleted'}))
            unset_jwt_cookies(response=response)

            return response

        return make_response(
            jsonify({'message': 'Unauthorized User'})), 401


class ForgotPasswordView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        current_token = get_jwt()['jti']
        if BlacklistToken.check_blacklist(current_token):
            responseObject = {
                'status': 'fail',
                'message': "Token has been Blacklisted. Log In again"
            }
            response = make_response(jsonify(responseObject)), 400
            return response
        current_user = get_jwt_identity()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=current_user).first()
            if user:
                token = create_access_token(
                    identity=user.email, expires_delta=False)

                reset_link = f'http://0.0.0.0:5000/reset-password?token={token}'
                msg = Message('Password Reset', sender=os.getenv('MAIL_USERNAME'),
                              recipients=[current_user])
                msg.body = f'Click the link below to reset your password:\n{reset_link}'
                mail.send(msg)

                responseObject = {
                    'status': 'success',
                    'message': 'Password reset email sent'
                }
                return make_response(jsonify(responseObject)), 200

            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class ResetPasswordView(MethodView):
    decorators = [jwt_required()]

    def post(self, token):
        current_token = get_jwt()['jti']
        if BlacklistToken.check_blacklist(current_token):
            responseObject = {
                'status': 'fail',
                'message': "Token has been Blacklisted. Log In again"
            }
            response = make_response(jsonify(responseObject)), 400
            return response
        token = token
        new_password = request.json.get('new_password')

        try:
            email = get_jwt_identity()
        except Exception:
            return make_response(jsonify({'message': 'Invalid or expired token'})), 400

        user = User.query.filter_by(email).first()
        if user:
            user.password = bcrypt.generate_password_hash(new_password)

            return make_response(jsonify({'message': 'Password reset successful'})), 200
        else:
            return make_response(jsonify({'message': 'User not found'})), 404


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')
delete_view = DeleteUserAPI.as_view('delete_user_api')
forget_pwd_view = ForgotPasswordView.as_view('forgot_password_api')
reset_pwd_view = ResetPasswordView.as_view('reset_pwd_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/users/<email>',
    view_func=delete_view,
    methods=['DELETE']
)
auth_blueprint.add_url_rule(
    '/auth/forget-password',
    view_func=forget_pwd_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/reset-password/<token>',
    view_func=reset_pwd_view,
    methods=['POST']
)
