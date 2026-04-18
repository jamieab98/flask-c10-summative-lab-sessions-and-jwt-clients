from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'Note {self.id}, {self.title}, {self.content}. Written by {self.user_id}'

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    notes = db.relationship('Note', backref='user')

    @property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = generate_password_hash(password)
    
    def authenticate(self, password):
        return check_password_hash(self._password_hash, password)