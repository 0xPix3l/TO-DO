from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

# Defining the maximum length for passwords
PASSWORD_MAX_LENGTH = 128

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(PASSWORD_MAX_LENGTH))
    todos = db.relationship('Todo', backref='author', lazy='dynamic')

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

