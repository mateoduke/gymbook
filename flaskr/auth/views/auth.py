from flask import request
from ..models import User, Token, auth_required
from ..resources import auth_bp


@auth_bp.route('/login', methods = ['POST'])

def login():
    """View for logging in a user"""
    request_json = request.get_json(silent=True)
    if not request_json:
        return {'error': 'username and password not provided in message body'}

    username = request_json.get('username', '')
    password = request_json.get('password', '')

    # Lookup user and validate credentials
    user = User.query.filter_by(username=username).first()
    user_authorized = User.check_user_password(user, password)
    if not user_authorized:
        return {'error':'User with credentials not found'}, 403

    # Lookup token and refresh token if it has expired
    user_token = Token.query.filter_by(user_id=user.id).first()
    if user_token:
        if not user_token.has_expired:
            return {'token': user_token.key}, 201
        user_token.delete()

    new_user_token = Token(user=user)
    new_user_token.save()
    return {'token': new_user_token.key}, 201


@auth_bp.route('/logout', methods = ['POST',])
@auth_required
def logout(user):
    user_token = Token.query.filter_by(user_id=user.id).first()
    if user_token:
        user_token.delete()

    return {}, 201
