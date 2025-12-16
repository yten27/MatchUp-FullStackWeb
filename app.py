import os
import db
import forms
from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import RegisterForm

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
@app.route('/register', methods=['GET', 'POST'])
def register():#neuen user hier anlegen: GET + POST
    # 1. Das Formular-Objekt vorbereiten
    form = forms.RegisterForm()
    
    # 2. Die große Entscheidung: Wurde der "Senden"-Knopf gedrückt UND ist alles richtig ausgefüllt?
    if form.validate_on_submit():
        db_con = db.get_db_con()
        
        # 3. Prüfen: Gibt es die Email schon?
        existing_user = db_con.execute("SELECT id FROM user WHERE email = ?", [form.email.data]).fetchone()
        if existing_user:
            flash('Diese Email ist bereits vergeben.', 'danger')
            return render_template('register.html', form=form) # Abbruch und zurück zum Formular

        # 4. Speichern (Der eigentliche Job)
        try:
            cursor = db_con.execute("INSERT INTO user (email, password) VALUES (?, ?)", 
                           [form.email.data, form.password.data])
            db_con.commit()
            
            # 5. Auto-Login (Session)
            new_user_id = cursor.lastrowid
            session['user_id'] = new_user_id
            
            flash('Erfolg!', 'success')
            return redirect(url_for('home')) # 6. Weiterleitung zur Startseite

        except Exception as e:
            flash(f'Fehler: {e}', 'danger')

    # 7. Das passiert ganz am Anfang (GET) ODER wenn Fehler im Formular sind
    return render_template('register.html', form=form)

#Match-Übersicht   
@app.route('/allmatches')
def allmatches():#matches anzeigen die in datenbank hinterlegt wurden, GET
    matches = db.get_all_matches()
    return render_template("allmatches.html", matches = matches)

#Match-Details , GET
@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    return render_template("match_detail.html", match_id=match_id)

#Create Match, GET + POST 
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