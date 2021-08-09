from enum import unique
from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow


login_manager = LoginManager()
ma = Marshmallow()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True, unique = True)
    email = db.Column(db.String(150), unique= True, nullable=False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, nullable = False, unique=True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    song = db.relationship('Song', backref = 'owner', lazy = True)
    
    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.get_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def get_token(self,length):
        return secrets.token_hex(length)

class Song(db.Model):
    id = db.Column(db.String, primary_key = True, unique = True)
    name = db.Column(db.String(150), unique= True, nullable=False)
    duration = db.Column(db.String(100), nullable = True)
    genre = db.Column(db.String, nullable = False)
    bpm = db.Column(db.String, nullable = False)
    key = db.Column(db.String, nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, duration, genre, bpm, key, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.duration = duration
        self.genre = genre
        self.bpm = bpm
        self.key = key
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())


class SongSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'duration', 'genre', 'bpm', 'key']

# Create a singular data ppoint return
song_schema = SongSchema()

# Create multiple data point return 
songs_schema = SongSchema(many = True)