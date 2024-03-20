from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddToCartForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()], default=1)
    submit = SubmitField('Add to Cart')

""" class UpdateCartForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update') """