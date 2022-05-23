from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from flaskr import ma
from ..models import Token


class TokenSchema(SQLAlchemyAutoSchema):
    expire_time = fields.DateTime(dump_only=True)

    class Meta:
        model = Token
        ordered = True
        fields = ('key','user', 'created_at', 'expire_time','_links')


    user = ma.URLFor('auth.user_detail', values=dict(id="<id>"))
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor('auth.token_detail', values=dict(id="<id>")),
        }
    )
