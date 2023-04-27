from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Find')
    submit1 = SubmitField('Clear')


class RegisterForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Password Again', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    file = FileField('Profile', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Registrer')


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EditProfile(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Change')
