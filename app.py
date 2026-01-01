import os
import db
from flask import Flask, render_template, redirect, url_for
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

#Match-Details , GET/ Läd machtes und participants/ unterscheidet owner oder joined/rendert detail view
@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    db_con = db.get_db_con()

    match = db_con.execute(
        "SELECT * FROM match WHERE id = ?",
        (match_id,)
    ).fetchone()

    if not match:
        return "Match not found", 404

    participants = db_con.execute(
        """
        SELECT u.id, u.email
        FROM user u
        JOIN match_participant mp ON u.id = mp.user_id
        WHERE mp.match_id = ?
        """,
        (match_id,)
    ).fetchall()

    participant_count = len(participants)
    price_per_person = (
        match["price"] / participant_count
        if participant_count > 0 else match["price"]
    )

    current_user_id = session.get("user_id")

    is_owner = current_user_id == match["host_user_id"]
    is_joined = any(p["id"] == current_user_id for p in participants)

    return render_template(
        "match_detail.html",
        match=match,
        participants=participants,
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
    created_matches = []
    joined_matches = []

    for match_id, match in matches.items():
        is_owner = match["host_user_id"] == current_user["id"]
        is_participant = any(
            p["id"] == current_user["id"]
            for p in participants.get(match_id, [])
        )
        if is_owner:
            created_matches.append(match)
        
        elif is_participant:
            my_matches.append(match)
            

    return render_template("my_matches.html",
    created_matches=created_matches,
    joined_matches=joined_matches
    )


#Buttons für match interaktion

# Join Match
@app.route("/matches/<int:match_id>/join", methods=["POST"])
def join_match(match_id):
    db_con = db.get_db_con()
    current_user_id = session["user_id"]

    db_con.execute(
        "INSERT INTO match_participant (user_id, match_id) VALUES (?, ?)",
        (current_user_id, match_id)
    )
    db_con.commit()

    return redirect(url_for("match_detail", match_id=match_id))
# Leave Match
@app.route("/matches/<int:match_id>/leave", methods=["POST"])
def leave_match(match_id):
    db_con = db.get_db_con()
    current_user_id = session["user_id"]

    db_con.execute(
        "DELETE FROM match_participant WHERE user_id = ? AND match_id = ?",
        (current_user_id, match_id)
    )
    db_con.commit()

    return redirect(url_for("match_detail", match_id=match_id))
# Cancel Match (nur Host)
@app.route("/matches/<int:match_id>/cancel", methods=["POST"])
def cancel_match(match_id):
    db_con = db.get_db_con()
    current_user_id = session["user_id"]

    db_con.execute(
        "DELETE FROM match WHERE id = ? AND host_user_id = ?",
        (match_id, current_user_id)
    )
    db_con.commit()

    return redirect(url_for("my_matches"))
#Nach Aufbau der Seite wird zum Schluss noch die Betragsfunktion, in welcher die Aufteilung des Preises noch geleistet wird