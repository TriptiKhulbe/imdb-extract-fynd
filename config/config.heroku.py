import os

# Rename this file to config.py
# For more - https://pythonhosted.org/Flask-Security/configuration.html

ENV = "development"
DEBUG = True
SECRET_KEY = "adfghytr43wfvdsfbgfnhrsthergsd"
SQLALCHEMY_ECHO = True

uri = os.environ['DATABASE_URL']
if uri.startswith("postgres://"):
  uri = uri.replace("postgres://", "postgresql://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECURITY_PASSWORD_SALT = ""
