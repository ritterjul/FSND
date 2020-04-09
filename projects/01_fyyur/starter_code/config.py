import os

SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgres://jule@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
