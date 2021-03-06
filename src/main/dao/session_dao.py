from dataclasses import asdict

from src.main.models.session import Session
from src.main import db


class SessionDAO:
    def __init__(self, user):
        self.access_token = user.access_token
        self.tokenized_user = asdict(user)

    def create(self):
        session = Session(
            access_token=self.access_token, tokenized_user=self.tokenized_user
        )
        db.session.add(session)
        db.session.commit()
        return self
