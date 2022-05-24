import click
import os
import json
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config = None):
    app = Flask(__name__, instance_relative_config=True)
    if config is None:
        app.config.from_object('config.DevelopmentConfig')
    elif config.get('TESTING', False):
        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)


    try:
        with app.app_context():
            from .auth import auth_bp
            from .auth.resources import UserResource, UserListResource
            from .auth.resources import TokenResource, TokenListResource
            from .auth.views import login, logout, routes
            auth_api = Api(auth_bp)
            auth_api.add_resource(UserListResource, '/users', endpoint = 'user_list')
            auth_api.add_resource(UserResource, '/users/<int:id>', endpoint = 'user_detail')
            auth_api.add_resource(TokenListResource, '/tokens', endpoint = 'token_list')
            auth_api.add_resource(TokenResource, '/tokens/<int:id>', endpoint = 'token_detail')

            app.register_blueprint(auth_bp)
            db.create_all()

        return app
    except AssertionError as ex:
        print(ex)
        if config.get('TESTING', False):
            return app
