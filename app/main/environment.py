import os

class Environment:
    ALLOWED_CORS_CLIENTS = ['*']
    SECRET_KEY = os.getenv('SECRET_KEY', 'lsarp_secret_key')
    MZXML_FILES_KEY_PREFIX = os.getenv('MZXML_FILES_KEY_PREFIX', 'mzxml_file_')
    MZXML_FILES_UPLOAD_FOLDER = os.getenv('MZXML_FILES_UPLOAD_FOLDER', '/tmp/')
    ALLOWED_MZXML_FILE_EXTENSIONS = os.getenv('ALLOWED_MZXML_FILE_EXTENSIONS', 'mzXML').split(',')
    ALLOWED_METADATA_SHIPMENTS_EXTENSIONS = os.getenv('ALLOWED_METADATA_SHIPMENTS_EXTENSIONS', 'xlsx').split(',')
    PAGINATION_MAX_PER_PAGE = os.getenv('PAGINATION_MAX_PER_PAGE', 100)
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
    ALLOWED_CORS_CLIENTS = os.getenv('ALLOWED_CORS_CLIENTS', 'https://resistancedb.org,http://proteomics.resistancedb.org').split(',')

environments = dict(
    development=Development,
    test=Test,
    production=Production
)

key = Environment.SECRET_KEY
