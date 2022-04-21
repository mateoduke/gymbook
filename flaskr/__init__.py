import click
import os

from flask import Flask


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

    # cli commands
    @app.cli.command('create-user')
    @click.argument('name')
    def create_user(name):
        print(name)

    @app.route('/')
    def hello():
        return 'Hello World'

    return app
