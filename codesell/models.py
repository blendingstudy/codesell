from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from codesell import db
#from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #password_hash = db.Column(db.String(128), nullable=False)

    """ @property
    def password(self):
        raise AttributeError('password is not a readable attribute') """

    """ @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) """

    def check_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return self.password == password

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class FundingProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    current_amount = db.Column(db.Integer, default=0)
    end_date = db.Column(db.String(120), nullable=False)