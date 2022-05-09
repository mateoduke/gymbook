from flask import current_app, request, Blueprint, jsonify
from flask_restful import Resource
from flaskr import db
from marshmallow import  ValidationError
from ..schemas import UserSchema
from ..models import User


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v2/auth')

class UserResource(Resource):
    """Resource for handling requests made to the /api/v2/auth/users/<id> endpoint"""
    user_schema = UserSchema()
    user_list_schema = UserSchema(many=True)

    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return {'errors': [f'User with id {id!r} not found']}, 404
        return self.user_schema.dump(user), 200


class UserListResource(Resource):
    """Resource for handling requests made to the /api/v2/auth/users endpoint"""
    user_schema = UserSchema()
    user_list_schema = UserSchema(many=True)

    def get(self):
        all_users = User.query.all()
        return self.user_list_schema.dump(all_users), 200


    def post(self):
        request_json = request.json
        try:
            user_context = self.user_schema.load(request_json)
        except ValidationError as ex:
            return {'errors': ex.messages}, 500


        if not user_context['valid']:
            return {'errors': user_context['errors']}, 400

        new_user = user_context['instance']
        db.session.add(new_user)
        db.session.commit()

        return self.user_schema.dump(new_user), 200
