
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    time_registered = db.Column(db.DateTime, nullable=False)
