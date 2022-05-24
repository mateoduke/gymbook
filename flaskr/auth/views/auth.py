from flask import request, current_app, url_for, jsonify
from ..models import User, Token, auth_required
from flaskr.auth import auth_bp



@auth_bp.route('/', methods=['GET',])
def routes():
    """Returns all routes for the endpoint"""
    prefix = auth_bp.name + '.'
    rules = current_app.url_map.iter_rules()
    for rule in rules:
        pass
    routes = [url_for(rule.endpoint) for rule in rules if rule.endpoint.startswith(prefix)]
    return jsonify(routes) , 200


@auth_bp.route('/login', methods = ['POST'])
def login():
    """View for logging in a user"""
    request_json = request.get_json(silent=True)
    if not request_json:
        return {'error': 'username and password not provided in message body'} , 400

    username = request_json.get('username', '')
    password = request_json.get('password', '')

    # Lookup user and validate credentials
    user = User.query.filter_by(username=username).first()
    user_authorized = User.check_user_password(user, password)

    if not user_authorized:
        return {'error':'User with credentials not found'}, 404

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
@auth_required()
def logout(user):
    user_token = Token.query.filter_by(user_id=user.id).first()
    if user_token:
        user_token.delete()

    return {}, 201
