from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .config import environments

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environments[environment])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app