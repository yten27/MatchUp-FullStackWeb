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
@app.route('/home')
def home():
    return render_template("home.html") #ähnlich wie main, lädt base.html grundlayout, GET

#Login
@app.route('/login')
def login(): #logik: GET + POST
    return render_template("login.html")

#Registrierung
@app.route('/register')
def register():#neuen user hier anlegen: GET + POST
    return render_template("register.html")

#Match-Übersicht   
@app.route('/allmatches')
def allmatches():#matches anzeigen die in datenbank hinterlegt wurden, GET
    
    return render_template("allmatches.html")

#Match-Details , GET
@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Create Match, GET + Post 
@app.route("/matches/create")
def create_match():
    return render_template("create_match.html")

#My Matches anzeigen, GET 
@app.route("/my-matches")
def my_matches():
    return render_template("my_matches.html")

#Join Match , Post
@app.route("/matches/<int:match_id>/join")
def join_match(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Leave Match , Post
@app.route("/matches/<int:match_id>/leave")
def leave_match(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Delete Match , Post, NUR HOST
@app.route("/matches/<int:match_id>/delete")
def delete_match(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Nach Aufbau der Seite wird zum Schluss noch die Betragsfunktion, in welcher die Aufteilung des Preises noch geleistet wird