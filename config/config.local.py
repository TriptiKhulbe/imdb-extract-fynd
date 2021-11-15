# Rename this file to config.py
# For more - https://pythonhosted.org/Flask-Security/configuration.html

ENV = "development"
DEBUG = True
SECRET_KEY = "adfghytr43wfvdsfbgfnhrsthergsd"
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = "sqlite:///api.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECURITY_PASSWORD_SALT = ""
