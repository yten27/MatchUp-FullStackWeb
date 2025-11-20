from flask import Flask, render_template
#Grundgerüst

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("base.html")#ähnlich wie main, lädt base.html grundlayout

#Login
@app.route('/login')
def login():#logik:
    return render_template("login.html")

#Registrierung
@app.route('/register')
def register():#neuen user hier anlegen:
    return render_template("register.html")

#Match-Übersicht   
@app.route('/match')
def match():#matches anzeigen die in datenbank hinterlegt wurden
    
    return render_template("match.html")

#Match-Details
@app.route('/match_details')
def match_details():#match details an

