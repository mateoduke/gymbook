import os

class Config(object):
    """Base Config object for flask project
    Other configs will inherit from this config
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    LOGIN_TIMEOUT_MINUTES = os.environ.get('LOGIN_TIMEOUT_MINUTES')
    LOGIN_TIMEOUT_HOURS = os.environ.get('LOGIN_TIMEOUT_HOURS')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    DEVELOPMENT = True
    SECRET_KEY = 'dev'


class ProductionConfig(Config):
    ENV = 'production'
    DEVELOPMENT = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    ENV = 'testing'
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_TIMEOUT_MINUTES = 10
    LOGIN_TIMEOUT_HOURS = 1
