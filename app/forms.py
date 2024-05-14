from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Optional, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    code_file = FileField('Code File', validators=[FileRequired(), FileAllowed(['zip', 'rar', 'tar.gz'], 'Only archive files are allowed!')])
    language = SelectField('Language', coerce=int, validators=[DataRequired()])
    usage = SelectField('Usage', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Product')

class FundingCreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    goal_amount = IntegerField('Goal Amount', validators=[DataRequired(), NumberRange(min=1)])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Create Funding')

class FundingUpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    goal_amount = IntegerField('Goal Amount', validators=[DataRequired(), NumberRange(min=1)])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Update Funding')

class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[Optional()])
    min_price = FloatField('Minimum Price', validators=[Optional(), NumberRange(min=0)])
    max_price = FloatField('Maximum Price', validators=[Optional(), NumberRange(min=0)])
    language = SelectField('Language', coerce=int, validators=[Optional()])
    usage = SelectField('Usage', coerce=int, validators=[Optional()])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', coerce=int, choices=[(i, str(i)) for i in range(1, 6)], validators=[DataRequired()])
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit Review')

class ProfileUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class ChatForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')