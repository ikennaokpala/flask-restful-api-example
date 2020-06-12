from app.main.models.session import Session
from app.main import db

class SessionDAO:
    def __init__(self, user):
        self.access_token = user.access_token
        self.tokenized_user = user._asdict()

    def create(self):
        session = Session(access_token=self.access_token, tokenized_user=self.tokenized_user)
        db.session.add(session)
        db.session.commit()
        return self