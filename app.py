import os
import db
from flask import Flask, render_template, redirect, url_for
#Grundgerüst

app = Flask(__name__)

#Dummy daten für match details 
current_user = {
    "id" : 1,
    "name": "Leon"
}

matches = {
  1: {  "id": 1,
    "title": "Fußball Turnier im Käfig",
    "location": "Seebenerstraße 16",
    "match_time": "2025-02-12 17:30",
    "price": 15,
    "host_user_id": 1
  }
}

participants = {
    1: [
        {"id": 1, "name": "Leon"},
        {"id": 2, "name": "Ayten"},
        {"id": 3, "name": "John"}

    ]
}

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

#Match-Details , GET/ Läd machtes und participants/ unterscheidet owner oder joined/rendert detail view
@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    match = matches.get(match_id)
    if not match:
        return "Match not found", 404

    match_participants = participants.get(match_id, [])

    participant_count = len(match_participants)
    price_per_person = (
    match["price"] / participant_count
    if participant_count > 0 else match["price"]
    )


    is_owner = match["host_user_id"] == current_user["id"]
    is_joined = any(p["id"] == current_user["id"] for p in match_participants)

    return render_template(
        "match_detail.html",
        match=match,
        participants=match_participants,
        is_owner=is_owner,
        is_joined=is_joined,
        price_per_person=price_per_person
    )



#Create Match, GET + Post 
@app.route("/matches/create")
def create_match():
    return render_template("create_match.html")

#My Matches anzeigen, GET 
@app.route("/my-matches")
def my_matches():
    user_id = current_user["id"]
    my_matches = []

    for match_id, match in matches.items():
        is_host = match["host_user_id"] == user_id
        is_participant = any(
            p["id"] == user_id
            for p in participants.get(match_id, [])
        )
        if is_host or is_participant:
            my_matches.append(match)
            

    return render_template("my_matches.html", matches=my_matches)


#Buttons für match interaktion

# Join Match
@app.route("/matches/<int:match_id>/join", methods=["POST"])
def join_match(match_id):
    return redirect(url_for("match_detail", match_id=match_id))


# Leave Match
@app.route("/matches/<int:match_id>/leave", methods=["POST"])
def leave_match(match_id):
    return redirect(url_for("match_detail", match_id=match_id))


# Cancel Match (nur Host)
@app.route("/matches/<int:match_id>/cancel", methods=["POST"])
def cancel_match(match_id):
    return redirect(url_for("match_detail", match_id=match_id))

#Nach Aufbau der Seite wird zum Schluss noch die Betragsfunktion, in welcher die Aufteilung des Preises noch geleistet wird