import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.main import create_app, db
from app.main.config.v1.routes import v1_blueprint
from app.main.environment import environments

app = create_app(os.getenv('BOILERPLATE_ENV') or 'development')
CORS(app)
app.register_blueprint(v1_blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0', port=3000)

@manager.command
def test_prepare():
    app.config.from_object(environments['test'])
    if database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])

@manager.command
def tests():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

test = tests

if __name__ == '__main__':
    manager.run()
