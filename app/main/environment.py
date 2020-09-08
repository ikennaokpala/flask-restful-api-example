import os

class Environment:
    TEST = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    LSARP_API_CORS_CLIENTS = ['*']
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'lsarp_secret_key')
    SEED_DATA_COUNT = int(os.getenv('SEED_DATA_COUNT', 100))
    PAGINATION_MAX_PER_PAGE = int(os.getenv('PAGINATION_MAX_PER_PAGE', 100))
    MZXML_FILES_UPLOAD_FOLDER = os.getenv('MZXML_FILES_UPLOAD_FOLDER', '/tmp/')
    MZXML_FILES_KEY_PREFIX = os.getenv('MZXML_FILES_KEY_PREFIX', 'mzxml_file_')
    DATA_FORMAT_FILE_EXTENSIONS = os.getenv('DATA_FORMAT_FILE_EXTENSIONS', 'mzXML,mzML,mzData,xlsx,csv,raw,BAF,DAT,FID,YEP,WIFF,XMS').split(',')
    METADATA_SHIPMENTS_FILE_COLUMNS = os.getenv('METADATA_SHIPMENTS_FILE_COLUMNS', 'DATE shipped,MATRIX_BOX,MATRIX_LOCN,ORGM,ISOLATE_NBR').split(',')
    TEST_DATA_COLLABORATORS = os.getenv('TEST_DATA_COLLABORATORS', 'dev@westgrid.ca,ikenna.okpala@computecanada.ca,patrick.mann@computecanada.ca,swacker@ucalgary.ca,snoskov@ucalgary.ca,ian.lewis2@ucalgary.ca,ian.percel@ucalgary.ca,fridman@ucalgary.ca').split(',')

class Development(Environment):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_development'

class Test(Environment):
    TEST = True
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_test'

class Production(Environment):
    DEBUG = False
    SEED_DATA_COUNT = 0
    TEST_DATA_COLLABORATORS = []
    SQLALCHEMY_DATABASE_URI = os.environ.get('LSARP_DATABASE_URL') + '/lsarp_production'
    LSARP_API_CORS_CLIENTS = os.getenv('LSARP_API_CORS_CLIENTS', 'https://resistancedb.org,http://proteomics.resistancedb.org').split(',')

environments = dict(
    development=Development,
    test=Test,
    production=Production
)

key = Environment.SECRET_KEY
