import os

from flask import current_app as app
from flask.cli import AppGroup
from sqlalchemy_utils import database_exists, create_database, drop_database

cli = AppGroup('db:')
environment = os.getenv('FLASK_ENV') or 'development'


@cli.command(short_help='Creates a database for the current flask environment')
def create():
    if environment == 'test' and database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])


@cli.command(short_help='Loads current database with seed/dummy data')
def seed():
    if environment in ['development', 'test'] and database_exists(
        app.config['SQLALCHEMY_DATABASE_URI']
    ):
        from app.data import Seed

        Seed.run()
    else:
        print('Something went wrong')


@cli.command(short_help='Drops the database for this flask environment')
def drop():
    drop_database(app.config['SQLALCHEMY_DATABASE_URI'])
