import datetime

from dataclasses import dataclass

from app.main import db

@dataclass
class Session(db.Model):
    __tablename__ = 'sessions'

    tokenized_user: dict

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.TEXT, index=True)
    tokenized_user = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
