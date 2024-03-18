import os

#BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'postgresql://kyounje:9350@localhost/codesell'
SQLALCHEMY_TRACK_MODIFICATIONS = False