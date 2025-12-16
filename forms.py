from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, Email

class RegisterForm(FlaskForm):
    # Email-Validierung prüft auf "@" und "."
    email = EmailField('Email Adresse', validators=[
        InputRequired(), 
        Email(message="Ungültige Email-Adresse")
    ])
    
    password = PasswordField('Passwort', validators=[
        InputRequired(), 
        Length(min=5, message="Mindestens 5 Zeichen.")
    ])
    
    confirm_password = PasswordField('Passwort wiederholen', validators=[
        InputRequired(), 
        EqualTo('password', message='Passwörter stimmen nicht überein.')
    ])
    
    submit = SubmitField('Registrieren')


class LoginForm(FlaskForm):
    # Email-Validierung prüft auf "@" und "."
    email = EmailField('Email Adresse', validators=[
        InputRequired(), 
        Email(message="Ungültige Email-Adresse")
    ])
    
    password = PasswordField('Passwort', validators=[
        InputRequired(), 
    ])
    
    submit = SubmitField('Registrieren')