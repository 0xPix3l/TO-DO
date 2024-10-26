import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/todo_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
