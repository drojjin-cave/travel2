from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    email = EmailField("Почта: ", validators=[Email()])
    name = StringField("Имя :  ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    password_again = PasswordField("Повторите \n пароль:", validators=[DataRequired()])
    old = IntegerField("Возраст :  ", validators=[DataRequired()])
    city = StringField("Город :  ", validators=[DataRequired()])
    register = SubmitField("Зарегистрироваться")


class LoginForm(FlaskForm):
    email = EmailField("Почта: ", validators=[Email()])
    password = PasswordField("Пароль: ", validators=[DataRequired()])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")
    def id(self):
        return None