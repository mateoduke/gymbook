import binascii
from datetime import datetime, timedelta
import os

from flask import request, jsonify, current_app
from flaskr import db
from functools import wraps
from sqlalchemy import  Column, ForeignKey, String, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class InvalidTokenError(Exception):
    """Raised when a given token is invalid"""


class Token(db.Model):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    key = Column(String(40), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='token')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    def __repr__(self):
        return self.key


    def save(self):
        """Saves token objects to database, generates
        key if token has not yet been created

        """
        if self.id is None:
            self.key = Token.generate_key()
            db.session.add(self)
        return db.session.commit()


    def delete(self):
        """Deletes token objects from database

        """
        db.session.delete(self)
        return db.session.commit()


    @property
    def has_expired(self):
        """Checks the current time vs time the token was created and determines if the token has expired
        or not.

        :return: True if expired, false if not
        :rtype: bool
        """
        return (datetime.utcnow() - self.created_at) > timedelta(hours=int(current_app.config['LOGIN_TIMEOUT_HOURS']),
                                                                minutes=int(current_app.config['LOGIN_TIMEOUT_MINUTES']))


    @property
    def expire_time(self):
        """Time at which this token expires"""
        return self.created_at + timedelta(hours=int(current_app.config['LOGIN_TIMEOUT_HOURS']),
                                                    minutes=int(current_app.config['LOGIN_TIMEOUT_MINUTES']))

    @staticmethod
    def generate_key():
        return binascii.hexlify(os.urandom(20)).decode()


    @staticmethod
    def get_token_from_header_context(context):
        """Takes in token context string, validates format and returns tokens

        :param context: String of format 'Token <Token String>'
        :return: Token string
        """
        token = context.split(' ')
        if len(token) != 2 or token[0] != 'Token':
            raise InvalidTokenError('Invalid Authorization Header')
        return token[1]


def auth_required(admin_required=False):
    """Decorator for wrapping view functions that require a user
    to be authenticated in order to access. View functions that
    implement this decorator must have a parameter called "user".
    This is an object representing the authenticated user

    :param admin_required: describes if view can only be accessed by admins, defaults to False
    :type admin_required: bool, optional
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token_context = request.headers.get('Authorization')
            if token_context:
                try:
                    token = Token.get_token_from_header_context(token_context)
                except InvalidTokenError as e:
                    return {'error': str(e)}, 400


                token_exists = Token.query.filter_by(key=token).first()
                if token_exists:
                    if token_exists.has_expired:
                        return {'error': 'Your token has expired, please login again'}, 401

                    if not token_exists.user.admin and admin_required:
                        return {'error': 'Access Restricted'}, 403

                    # adds the authenticated user to the view function kwargs
                    kwargs['user'] = token_exists.user
                    return f(*args, **kwargs)

                return {'error': 'invalid token'}, 403
            return {'error': 'Token not provided'}, 403
        return wrapper
    return decorator
