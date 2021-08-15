from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), validators.Length(min=4, max=30, message="4 - 30 characters"), validators.Email(message="Invalid email address")])
    password = PasswordField(label="Password", validators=[DataRequired(), validators.Length(min=8, message="At least 8 characters")])
    submit = SubmitField(label="Log In")
