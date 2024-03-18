""" import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) """

from codesell import db
from codesell.models import User

def authenticate_user(username, password):
    user = User.query.filter_by(username=username, password=password).first()
    return user

def register_user(username, password):
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()