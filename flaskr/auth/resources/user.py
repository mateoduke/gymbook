from flask import current_app, request, Blueprint, jsonify
from flask_restful import Resource
from marshmallow import  ValidationError


from ..schemas import UserSchema
from ..models import User, Token, InvalidTokenError, auth_required, admin_required


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v2/auth')

class UserResource(Resource):
    """Resource for handling requests made to the /api/v2/auth/users/<id> endpoint"""
    user_schema = UserSchema()
    user_list_schema = UserSchema(many=True)

    @admin_required
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return {'errors': [f'User with id {id!r} not found']}, 404
        return self.user_schema.dump(user), 200


class UserListResource(Resource):
    """Resource for handling requests made to the /api/v2/auth/users endpoint"""
    user_schema = UserSchema()
    user_list_schema = UserSchema(many=True)

    @admin_required
    def get(self, user):
        all_users = User.query.all()
        return self.user_list_schema.dump(all_users), 200


    def post(self):
        request_json = request.get_json(silent=True)

        # Check if user is attempting to create an admin user
        if request_json and request_json.get('admin', True):
            auth_context = request.headers.get('Authorization', '')
            try:
                parsed_token_str = Token.get_token_from_header_context(auth_context)
            except InvalidTokenError as ex:
                parsed_token_str = ''
            token = Token.query.filter_by(key=parsed_token_str).first()
            if not token or not token.user.admin:
                return {'error': 'Only admin users have permission to create admins'}, 403

        try:
            user_context = self.user_schema.load(request_json)
        except ValidationError as ex:
            return {'errors': ex.messages}, 500


        if not user_context['valid']:
            return {'errors': user_context['errors']}, 400

        new_user = user_context['instance']
        user_token = Token(user=new_user)
        user_token.save()
        new_user.save()

        return self.user_schema.dump(new_user), 200

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
