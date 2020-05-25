import os

class Environment:
    SECRET_KEY = os.getenv('SECRET_KEY', 'lsarp_secret_key')
    DEBUG = False
    TEST = False
    SQLALCHEMY_DATABASE_URI = ''
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Environment):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_development'

class Test(Environment):
    DEBUG = True
    TEST = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_test'

class Production(Environment):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_production'

environments = dict(
    development=Development,
    test=Test,
    production=Production
)

key = Environment.SECRET_KEY
