import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from logging.config import dictConfig

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config = None):
    app = Flask(__name__, instance_relative_config=True)

    if config is None:
        app.config.from_object('config.DevelopmentConfig')
    elif config.get('TESTING', False):
        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s][%(levelname)s] %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    try:
        os.makedirs(app.instance_path)
    except OSError as ex:
        app.logger.debug(f'Could not create directory {app.instance_path} due to following error:\n {ex}')

    db.init_app(app)
    migrate.init_app(app, db)


    try:
        with app.app_context():
            from .auth import auth_bp
            from .auth.resources import UserResource, UserListResource
            from .auth.resources import TokenResource, TokenListResource
            from .auth.views import login, logout, routes
            from .auth.commands import create_user
            auth_api = Api(auth_bp)
            auth_api.add_resource(UserListResource, '/users', endpoint = 'user_list')
            auth_api.add_resource(UserResource, '/users/<int:id>', endpoint = 'user_detail')
            auth_api.add_resource(TokenListResource, '/tokens', endpoint = 'token_list')
            auth_api.add_resource(TokenResource, '/tokens/<int:id>', endpoint = 'token_detail')

            app.register_blueprint(auth_bp)
            db.create_all()

        return app
    except AssertionError as ex:
        app.logger.error(str(ex))
        if config.get('TESTING', False):
            return app
