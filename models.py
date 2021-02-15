import os
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    session_token = db.Column(db.String)
    deleted = db.Column(db.Boolean, default=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    surname = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String, unique=True)
    city = db.Column(db.String, unique=False)
