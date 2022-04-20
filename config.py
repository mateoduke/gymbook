import os

class Config(object):
    """Base Config object for flask project
    Other configs will inherit from this config
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

class DevelopmentConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    SECRET_KEY = 'dev'
