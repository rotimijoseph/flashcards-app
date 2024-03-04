from app import db

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32))
    surname = db.Column(db.String(32), nullable=False, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password = db.Column(db.String(20), nullable=False)