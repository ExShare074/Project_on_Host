from app import db
from app import login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    login_attempts = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    is_locked_until = db.Column(db.DateTime)

    def __repr__(self):
        return f"User'{self.username}', '{self.clicks}'"

@login_manager.user_loader
def load(user_id):
    return User.query.get(int(user_id))