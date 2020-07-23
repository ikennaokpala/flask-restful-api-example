import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_restplus import Api
from flask_script import Manager

from sqlalchemy_utils import database_exists, create_database, drop_database

from app.main import create_app, db
from app.main.config.v1.routes import v1_blueprint, RouterV1
from app.main.environment import environments

environment = os.getenv('FLASK_ENV') or 'development'

app = create_app(environment)
app.register_blueprint(v1_blueprint)
app.app_context().push()

authorizations = {
    'authorization': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'accessToken': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-ACCESS-TOKEN'
    },
    'oauth2': {
        'type': 'oauth2',
        'flow': 'accessCode',
    }
}

swagger_ui = Api(app,
    title='LSARP API Documentation',
    version='1.0',
	description='This is backend API documentation for the LSARP project. Prefix all endpoints with /v1',
	security=['accessToken', 'oauth2'],
	authorizations=authorizations
)
RouterV1().draw(swagger_ui)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', port=3000)

@manager.command
def dropdb(environment):
    app.config.from_object(environments[environment])
    drop_database(app.config['SQLALCHEMY_DATABASE_URI'])

@manager.command
def createdb(environment):
    app.config.from_object(environments[environment])
    if environment == 'test' and database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

@manager.command
def tests():
    """Runs the unit tests."""
    app.config.from_object(environments['test'])
    createdb('test')
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

test = tests

if __name__ == '__main__':
    manager.run()
