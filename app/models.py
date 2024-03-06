from app import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32))
    surname = db.Column(db.String(32), nullable=False, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password = db.Column(db.String(20), nullable=False)
    
    def get_id(self):
        return str(self.user_id)
    
# re loading user from user id stored in the session 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class FlashCard(db.Model):
    __tablename__ = "flashcards"
    flashcard_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100), nullable=False)
    answer = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)