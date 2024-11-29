from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    key = db.Column(db.String, unique=True, nullable=False)
    files = db.relationship("File",back_populates="user",cascade="all, delete-orphan")

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_filename = db.Column(db.String, nullable=False)
    encrypt_filename = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User",back_populates="files")

