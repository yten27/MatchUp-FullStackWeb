import os
import db
from flask import Flask, render_template
#Grundgerüst

app = Flask(__name__)

#Für Datenbankanbindung:
app.config.from_mapping(
    SECRET_KEY='secret_key_just_for_dev_environment',
    DATABASE=os.path.join(app.instance_path, 'matchup.sqlite')
)
app.cli.add_command(db.init_db)
app.teardown_appcontext(db.close_db_con)

#Rein für die Testung von DB
@app.route("/insert/sample")
def run_insert_sample():
    db.insert_sample()
    return "Database flushed and populated with some sample MatchUp data."



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

   return render_template("match_details.html")