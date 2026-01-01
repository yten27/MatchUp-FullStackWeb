from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, EmailField, StringField, DateTimeLocalField, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Email, NumberRange

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

class CreateMatchForm(FlaskForm):
    title = StringField('Titel / Spielmodus', validators=[
        InputRequired(),
        Length(min=3, message="Der Titel ist zu kurz.")
    ])
    
    location = StringField('Ort / Bolzplatz', validators=[
        InputRequired()
    ])
    
    # format='%Y-%m-%dT%H:%M' ist der Standard-Code für HTML5-Kalender
    match_time = DateTimeLocalField('Anpfiff', format='%Y-%m-%dT%H:%M', validators=[
        InputRequired()
    ])

    price = IntegerField(
        'Gesamtpreis ($)',
        validators=[
            InputRequired(),
            NumberRange(min=0)
        ]
    )
    
    submit = SubmitField('Match erstellen')