import os
from flask import Flask

def create_app(config = None):
    app = Flask(__name__, instance_relative_config=True)
    if config is None:
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_mapping(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello World'

    return app
