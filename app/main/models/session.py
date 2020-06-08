from app.main import db

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    tokenized_user = db.Column(JSON)