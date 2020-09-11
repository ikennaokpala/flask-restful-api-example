import os
import click

from flask.cli import FlaskGroup
from flask_migrate import Migrate
from flask_restx import Api

from src.main import create_app, db
from src.main.config.tasks.db import cli as commands
from src.main.config.v1.routes import v1_blueprint, RouterV1

MIGRATION_DIR = os.path.join('src', 'main', 'config', 'db', 'migrations')

app = create_app()
app.register_blueprint(v1_blueprint)
app.app_context().push()

Migrate(app, db, directory=MIGRATION_DIR)

authorizations = {
    'authorization': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'},
    'accessToken': {'type': 'apiKey', 'in': 'header', 'name': 'X-ACCESS-TOKEN'},
    'oauth2': {'type': 'oauth2', 'flow': 'accessCode'},
}

swagger_ui = Api(
    app,
    title='LSARP API Documentation',
    version='1.0',
    description='This is backend API documentation for the LSARP project.',
    security=['accessToken', 'oauth2'],
    authorizations=authorizations,
)
RouterV1().draw(swagger_ui, prefix='/v1')


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Main entry point"""
    pass


app.cli.add_command(commands)
application = app  # Used by uWSGI to create a production instance

if __name__ == '__main__':
    cli()
