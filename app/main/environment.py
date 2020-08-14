import os

class Environment:
    ALLOWED_CORS_CLIENTS = ['*']
    SECRET_KEY = os.getenv('SECRET_KEY', 'lsarp_secret_key')
    MZXML_FILES_KEY_PREFIX = os.getenv('MZXML_FILES_KEY_PREFIX', 'mzxml_file_')
    MZXML_FILES_UPLOAD_FOLDER = os.getenv('MZXML_FILES_UPLOAD_FOLDER', '/tmp/')
    DATA_FORMAT_FILE_EXTENSIONS = os.getenv('DATA_FORMAT_FILE_EXTENSIONS', 'mzXML,mzML,mzData,xlsx,csv,raw,BAF,DAT,FID,YEP,WIFF,XMS').split(',')
    PAGINATION_MAX_PER_PAGE = int(os.getenv('PAGINATION_MAX_PER_PAGE', 100))
    DEBUG = False
    TEST = False
    SQLALCHEMY_DATABASE_URI = ''
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Environment):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_development'

class Test(Environment):
    TEST = True
    DEBUG = True
    TESTING = True
    TEST_PROGRESS_VERBOSITY = int(os.getenv('TEST_PROGRESS_VERBOSITY', 1))
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
