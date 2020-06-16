import os 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .environment import environments

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

CUSTOM_REQUEST_HEADERS = ['Authorization', 'X-ACCESS-TOKEN']

def create_app(environment):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.urandom(24))
    app.config.from_object(environments[environment])
    CORS(app, resources={r'/v1/*': { 'origins': app.config['ALLOWED_CORS_CLIENTS'] }}, headers=CUSTOM_REQUEST_HEADERS, expose_headers=CUSTOM_REQUEST_HEADERS)
    
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app
