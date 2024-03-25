import os

#BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
SQLALCHEMY_DATABASE_URI = 'postgresql://kyounje:9350@localhost/codesell'
SQLALCHEMY_TRACK_MODIFICATIONS = False

IAMP_KEY = '0054575041252252'
IAMP_SECRET = '4y5PCQ5KoXFWRL7UltBruL2pvSnux1jjVFwo2L5hFqCNYH4AJGjXsCPbmGezWzwnWkHNP7Uv4ApDwb4w' 