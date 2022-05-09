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
    else:
        app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)


    with app.app_context():
        from .auth.resources import auth_bp, UserResource, UserListResource
        api = Api(auth_bp)
        api.add_resource(UserListResource, '/users', endpoint = 'user_list')
        api.add_resource(UserResource, '/users/<int:id>', endpoint = 'user_detail')
        db.create_all()

    app.register_blueprint(auth_bp)

    return app
