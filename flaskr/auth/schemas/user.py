from marshmallow import post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from werkzeug.security import generate_password_hash
from flaskr import ma
from ..models import User

class UserSchema(SQLAlchemyAutoSchema):
    """Schema for serializing and deserializing User instances"""
    password = auto_field(load_only=True)
    registered_on = auto_field(dump_only=True)

    class Meta:
        model = User
        ordered = True
        fields = ('username', 'first_name', 'password','last_name', 'admin', 'registered_on', '_links')

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor('auth.user_detail', values=dict(id="<id>")),
        }
    )

    def validate(self, data):
        """Validation function for incomming request json. Ensures that data from request
        is valid for creating a new user. If any data is not valid, an error will be appended
        and returned.

        :param data: json data from request
        :type data: dict
        :return: Whether or not
        :rtype: _type_
        """
        errors = []

        username = data.get('username')
        password = data.get('password')
        user_queryset = User.query.filter_by(username = username)
        if password is None:
            errors.append('Password is required to create account')

        if len(password) < 12:
            errors.append('Password must be at least 12 characters long')


        if user_queryset.count() > 0:
            errors.append(f'Username {username!r} has already been used')


        return len(errors) == 0, errors

    @post_load
    def create_user_context(self, data, **kwargs):
        """Creates user context based on supplied json data

        :param data: json request body from post request
        :type data: dict
        :return: context containing whether json was valid and errors/User instance
        :rtype: dict
        """
        valid, errors = self.validate(data)
        if not valid:
            return {'valid': valid, 'errors': errors}

        data['password'] = generate_password_hash(data['password'])
        return {'valid': valid, 'instance':User(**data)}
