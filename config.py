import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://kyounje:9350@localhost/codesell2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 추가 설정 옵션들
    # ...