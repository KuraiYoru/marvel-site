from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Искать')
    submit1 = SubmitField('Сброосить')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Пароль', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    file = FileField('Profile', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Зарегистрироваться')
