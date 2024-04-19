import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://kyounje:9350@localhost/codesell2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 추가 설정 옵션들
    # ...

    # 펀딩 관련 설정
    FUNDING_COMMISSION_RATE = 0.05  # 펀딩 수수료율 (5%)
    FUNDING_GOAL_ACHIEVED_THRESHOLD = 0.9  # 펀딩 목표 달성 임계값 (90%)