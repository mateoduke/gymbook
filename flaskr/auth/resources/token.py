from flask_restful import Resource
from ..schemas import TokenSchema
from ..models import Token, auth_required


class TokenResource(Resource):
    token_schema = TokenSchema()
    token_list_schema = TokenSchema(many=True)

    @auth_required(admin_required=True)
    def get(self, id, user):
        token = Token.query.get(id)
        return self.token_schema.dump(token), 200


class TokenListResource(Resource):
    token_schema = TokenSchema()
    token_list_schema = TokenSchema(many=True)

    @auth_required(admin_required=True)
    def get(self, user):
        tokens = Token.query.all()
        return self.token_list_schema.dump(tokens), 200
