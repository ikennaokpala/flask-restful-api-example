import os 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .environment import environments

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(environment):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.urandom(24))
    app.config.from_object(environments[environment])
    CORS(app)
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
