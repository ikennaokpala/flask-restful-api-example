import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_restplus import Api

from sqlalchemy_utils import database_exists, create_database, drop_database

from app.main import create_app, db
from app.main.config.v1.routes import v1_blueprint
from app.main.environment import environments

from app.main.controllers.v1.auth_controller import endpoint as auth_endpoint
from app.main.controllers.v1.projects_controller import endpoint as projects_endpoint
from app.main.controllers.v1.project_raw_files_controller import endpoint as project_raw_files_endpoint

environment = os.getenv('FLASK_ENV') or 'development'

app = create_app(environment)
app.register_blueprint(v1_blueprint, url_prefix='/v1')
api = Api(app,
          title='LSARP API',
          version='1.0',
          description='This is the backend API implementation for the LSARP project'
          )
app.app_context().push()
api.add_namespace(auth_endpoint, path='/auth')
api.add_namespace(projects_endpoint, path='/projects')
api.add_namespace(project_raw_files_endpoint, path='/projects/<slug>')

# api.add_namespace(auth_endpoint, path='/v1/auth')
# api.add_namespace(projects_endpoint, path='/v1/projects')
# api.add_namespace(project_raw_files_endpoint, path='/v1/projects/<slug>')

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
