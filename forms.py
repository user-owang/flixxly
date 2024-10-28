from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, InputRequired, URL, Optional

class AddUserForm(FlaskForm):
    """form for user registration"""

    username = StringField("Username*", validators=[InputRequired(), Length(max=25, message='Username cannot exceed 25 characters')])
    password = PasswordField('Password*', validators=[InputRequired(), Length(max=20, min=8)])
    confirm_password = PasswordField('Confirm Password*', validators=[InputRequired(), Length(max=20, min=8)])
    email = StringField('Email*', validators=[InputRequired(), Email(message='Please enter a valid email address'), Length(max=50, message='Email cannot exceed 50 characters')])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[Length(max=20)])

class EditProfileForm(FlaskForm):
    """Edit profile form"""

    username = StringField("Username*", validators=[InputRequired(), Length(max=25, message='Username cannot exceed 25 characters')])
    email = StringField('Email*', validators=[InputRequired(), Email(message='Please enter a valid email address'), Length(max=50, message='Email cannot exceed 50 characters')])
    bio = StringField("Bio", validators=[Optional(), Length(max=100, message='Cannot exceed 100 characters')])
    img_url = StringField('Profile Picture URL', validators=[Optional(), URL(message='Please enter a valid image URL')])
    confirm_password = PasswordField('Confirm Password*', validators=[InputRequired(), Length(max=20, min=8)])