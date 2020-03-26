from app import db,login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teams = db.Column(db.String(140)) # possibly a foreign key to another Teams class
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cash = db.Column(db.Integer)

    def __repr__(self):
        return '<Portfolio {}>'.format(self.teams)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))