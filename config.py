import os

from flask_sqlalchemy import SQLAlchemy

class Config(object):
    """Base Config object for flask project
    Other configs will inherit from this config
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class DevelopmentConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    SECRET_KEY = 'dev'


class ProductionConfig(Config):
    ENV = 'production'
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
