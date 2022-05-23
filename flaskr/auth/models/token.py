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
        if self.id is None:
            self.key = Token.generate_key()
            db.session.add(self)
        return db.session.commit()


    def delete(self):
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



def auth_required(f):
    """Decorator for view functions that require the user to provide an authentication token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token_context = request.headers.get('Authorization')
        if token_context:
            try:
                token = Token.get_token_from_header_context(token_context)
            except InvalidTokenError as e:
                return jsonify({'error': str(e)}), 400


            token_exists = Token.query.filter_by(key=token).first()
            if token_exists:
                if token_exists.has_expired:
                    return {'error': 'Your token has expired, please login again'}, 401
                kwargs['user'] = token_exists.user
                return f(*args, **kwargs)

            return {'error': 'invalid token'}, 403
        return {'error': 'Token not provided'}, 403
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_context = request.headers.get('Authorization')
        if token_context:
            try:
                token = Token.get_token_from_header_context(token_context)
            except InvalidTokenError as e:
                return jsonify({'error': str(e)}), 400


            token_exists = Token.query.filter_by(key=token).first()
            if token_exists:
                if token_exists.has_expired:
                    return {'error': 'Your token has expired, please login again'}, 401

                if not token_exists.user.admin:
                    return jsonify({'error': 'Access Restricted'}), 403

                kwargs['user'] = token_exists.user
                return f(*args, **kwargs)

            return {'error': 'invalid token'}, 403
        return {'error': 'Token not provided'}, 403
    return decorated
